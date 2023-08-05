from dataclasses import dataclass
import enum
import os
from pathlib import Path as ImpurePath, PurePath
import re
import subprocess
import sys
from typing import Dict, List, Optional, Set, TextIO, Tuple, Any, Union

from .token import *
from ..args import Args
from ..util import PeekableIterator

__all__ = [
    'Makefile',
]

@dataclass()
class Makefile:
    _inference_rules: List['InferenceRule']
    _macros: Dict[str, Tuple['MacroSource', TokenString]]
    _targets: Dict[str, 'Target']
    first_non_special_target: Optional[str]
    args: Args
    _warnings: Set[str]

    def __init__(self, args: Args):
        self._inference_rules = []
        self._macros = dict()
        self._targets = dict()
        self.first_non_special_target = None
        self.args = args
        self._warnings = set()

        if args.builtin_rules:
            self._inference_rules += BUILTIN_INFERENCE_RULES
            for k, v in BUILTIN_MACROS.items():
                if isinstance(v, TokenString):
                    v_tokens = v
                else:
                    v_tokens = TokenString.text(v)
                self._macros[k] = (MacroSource.Builtin, v_tokens)
            for target in BUILTIN_TARGETS:
                self._targets[target.name] = target

        for k, v in os.environ.items():
            if k not in ['MAKEFLAGS', 'SHELL']:
                self._macros[k] = (MacroSource.Environment, TokenString.text(v))

        for target_or_macro in args.targets_or_macros:
            if '=' in target_or_macro:
                # it's a macro
                name, value = target_or_macro.split('=', 1)
                # TODO either discern command line vs MAKEFLAGS or don't pretend we can
                self._macros[name] = (MacroSource.CommandLine, TokenString.text(value))

    def __str__(self) -> str:
        def header(text: str) -> str:
            return text + '\n' + ('=' * len(text))
        return '\n'.join([
            header('Inference Rules'),
            *[str(x) for x in self._inference_rules],
            '',
            header('Macros'),
            *[f'{k}={v}' for k, (_, v) in self._macros.items()],
            '',
            header('Targets'),
            *[str(x) for x in self._targets.values()],
        ])

    def _warn(self, warning: str) -> None:
        if warning not in self._warnings:
            print(warning)
            self._warnings.add(warning)

    def read(self, file: TextIO) -> None:
        lines_iter: PeekableIterator[str] = PeekableIterator(iter(file))
        for line in lines_iter:
            # handle escaped newlines (POSIX says these are different in command lines (which we handle later) and
            # does not define if they are different in include lines (so we treat them as the same)
            while line.endswith('\\\n'):
                line = line[:-2] + next(lines_iter, '').lstrip()

            # POSIX:
            # > If the word include appears at the beginning of a line and is followed by one or more <blank>
            # > characters...
            if line.startswith('include '):
                # > the string formed by the remainder of the line...
                line = line[len('include '):].lstrip()
                # > shall be processed as follows to produce a pathname:

                # > The trailing <newline>, any <blank> characters immediately preceding a comment, and any comment
                # > shall be discarded.
                line = re.sub(r'(\s+#.*)?\n', '', line)

                # > The resulting string shall be processed for macro expansion.
                line = self.expand_macros(tokenize(line))

                # > Any <blank> characters that appear after the first non- <blank> shall be used as separators to
                # > divide the macro-expanded string into fields.
                fields = line.split()

                # > If the processing of separators and optional pathname expansion results in either zero or two or
                # > more non-empty fields, the behavior is unspecified. If it results in one non-empty field, that
                # > field is taken as the pathname.
                # (GNU make will include each field separately, so let's do that here)
                if len(fields) != 1:
                    self._warn('warning: non-POSIX multi-file include')
                for included_file in fields:
                    # > The contents of the file specified by the pathname shall be read and processed as if they
                    # > appeared in the makefile in place of the include line.
                    self.read(open(included_file, 'r'))

                # make sure we don't process an ambiguous line as both an include and something else
                continue

            # TODO figure out if this is always safe here
            line = line.rstrip('\n')

            # decide if this is a macro or rule
            line_type = 'unknown'
            line_tokens = tokenize(line)
            for t in line_tokens:
                if isinstance(t, TextToken):
                    if ':' in t.text and ('=' not in t.text or t.text.index(':') < t.text.index('=')):
                        line_type = 'rule'
                        break
                    elif '=' in t.text and (':' not in t.text or t.text.index('=') < t.text.index(':')):
                        line_type = 'macro'
                        break

            if line_type == 'rule':
                # > Target entries are specified by a <blank>-separated, non-null list of targets, then a <colon>, then
                # > a <blank>-separated, possibly empty list of prerequisites.
                colon_split = line_tokens.split_once(':')
                assert colon_split is not None
                targets_tokens, after_colon = colon_split
                targets = self.expand_macros(targets_tokens).split()
                # > Text following a <semicolon>, if any, and all following lines that begin with a <tab>, are makefile
                # > command lines to be executed to update the target.
                semicolon_split = after_colon.split_once(';')
                if semicolon_split is None:
                    prerequisites = self.expand_macros(after_colon).split()
                    command_token_strings = []
                else:
                    prerequisite_tokens, command_tokens = semicolon_split
                    prerequisites = self.expand_macros(prerequisite_tokens).split()
                    # TODO handle escaped newline in this case
                    command_token_strings = [command_tokens]
                while (peeked := lines_iter.peek()) is not None and peeked.startswith('\t'):
                    next_line = next(lines_iter)
                    # > When an escaped <newline> is found in a command line in a makefile, the command line shall
                    # > contain the <backslash>, the <newline>, and the next line, except that the first character of
                    # > the next line shall not be included if it is a <tab>.
                    while next_line.endswith('\\\n'):
                        line_after = next(lines_iter)
                        if line_after.startswith('\t'):
                            line_after = line_after[1:]
                        next_line += line_after
                    command_token_strings.append(tokenize(next_line.lstrip('\t').rstrip('\n')))
                commands = [CommandLine(c) for c in command_token_strings]

                # we don't know yet if it's a target rule or an inference rule
                match = re.fullmatch(r'(?P<s2>(\.[^/.]+)?)(?P<s1>\.[^/.]+)', targets[0])
                # we don't want to catch special targets, though
                special_target_match = re.fullmatch(r'\.[A-Z]+', targets[0])
                if len(targets) == 1 and len(prerequisites) == 0 and match is not None and special_target_match is None:
                    # it's an inference rule!
                    new_rule = InferenceRule(match.group('s1'), match.group('s2'), commands)
                    rules = [r for r in self._inference_rules if (r.s1, r.s2) != (new_rule.s1, new_rule.s2)]
                    self._inference_rules = rules
                    self._inference_rules.append(new_rule)
                else:
                    # it's a target rule!
                    for target in targets:
                        if self.first_non_special_target is None and not target.startswith('.'):
                            self.first_non_special_target = target
                        # > A target that has prerequisites, but does not have any commands, can be used to add to the
                        # > prerequisite list for that target.
                        # but also
                        # > If .SUFFIXES does not have any prerequisites, the list of known suffixes shall be cleared.
                        if target in self._targets and len(commands) == 0 and \
                                not (target == '.SUFFIXES' and len(prerequisites) == 0):
                            for new_prereq in prerequisites:
                                if new_prereq not in self._targets[target].prerequisites:
                                    self._targets[target].prerequisites.append(new_prereq)
                        else:
                            self._targets[target] = Target(target, prerequisites, commands)
            elif line_type == 'macro':
                # > The macro named string1 is defined as having the value of string2, where string2 is defined as all
                # > characters, if any, after the <equals-sign>...
                equals_split = line_tokens.split_once('=')
                assert equals_split is not None
                name_tokens, value = equals_split
                # > up to a comment character ( '#' ) or an unescaped <newline>.
                comment_split = value.split_once('#')
                if comment_split is not None:
                    value, _ = comment_split
                # GNU make allows for weird assignment operators
                expand_value = False
                skip_if_defined = False
                append = False
                if name_tokens.endswith('::'):
                    self._warn('warning: non-POSIXful `::=` in macro')
                    name_tokens.rstrip(':')
                    expand_value = True
                elif name_tokens.endswith(':'):
                    self._warn('warning: non-POSIXful `:=` in macro')
                    name_tokens.rstrip(':')
                    expand_value = True
                elif name_tokens.endswith('?'):
                    self._warn('warning: non-POSIXful `?=` in macro')
                    name_tokens.rstrip('?')
                    skip_if_defined = True
                elif name_tokens.endswith('+'):
                    self._warn('warning: non-POSIXful `+=` in macro')
                    name_tokens.rstrip('+')
                    append = True
                # > Any <blank> characters immediately before or after the <equals-sign> shall be ignored.
                name_tokens.rstrip()
                value.lstrip()
                # > Macros in the string before the <equals-sign> in a macro definition shall be evaluated when the
                # > macro assignment is made.
                name = self.expand_macros(name_tokens)
                if expand_value:
                    value = TokenString.text(self.expand_macros(value))
                # > Macros defined in the makefile(s) shall override macro definitions that occur before them in the
                # > makefile(s) and macro definitions from source 4. If the -e option is not specified, macros defined
                # > in the makefile(s) shall override macro definitions from source 3. Macros defined in the makefile(s)
                # > shall not override macro definitions from source 1 or source 2.
                if name in self._macros:
                    if skip_if_defined:
                        continue
                    source, _ = self._macros[name]
                    inviolate_sources = [MacroSource.CommandLine, MacroSource.MAKEFLAGS]
                    if self.args.environment_overrides:
                        inviolate_sources.append(MacroSource.Environment)
                    if any(x is source for x in inviolate_sources):
                        continue
                if append and name in self._macros:
                    _, old_value = self._macros[name]
                    value = old_value.concat(TokenString.text(' ')).concat(value)
                self._macros[name] = (MacroSource.File, value)

    def expand_macros(self, text: TokenString, current_target: Optional['Target'] = None) -> str:
        def expand_one(this_token: Token) -> str:
            if isinstance(this_token, TextToken):
                return this_token.text
            elif isinstance(this_token, MacroToken):
                macro_name = this_token.name
                internal_macro = len(macro_name) in [1, 2] and macro_name[0] in '@?<*' and \
                                 macro_name[1:] in ['', 'D', 'F']
                if internal_macro:
                    assert current_target is not None
                    if macro_name[0] == '@':
                        # > The $@ shall evaluate to the full target name of the current target, or the archive filename
                        # > part of a library archive target. It shall be evaluated for both target and inference rules.
                        macro_pieces = [current_target.name]
                    elif macro_name[0] == '?':
                        # > The $? macro shall evaluate to the list of prerequisites that are newer than the current
                        # > target. It shall be evaluated for both target and inference rules.
                        macro_pieces = [p for p in current_target.prerequisites if self.target(p).newer_than(current_target)]
                    elif macro_name[0] == '<':
                        # > In an inference rule, the $< macro shall evaluate to the filename whose existence allowed
                        # > the inference rule to be chosen for the target. In the .DEFAULT rule, the $< macro shall
                        # > evaluate to the current target name.
                        macro_pieces = current_target.prerequisites
                    elif macro_name[0] == '*':
                        # > The $* macro shall evaluate to the current target name with its suffix deleted.
                        macro_pieces = [str(PurePath(current_target.name).with_suffix(''))]
                    else:
                        # this shouldn't happen
                        macro_pieces = []

                    if macro_name[1:] == 'D':
                        macro_pieces = [str(PurePath(x).parent) for x in macro_pieces]
                    elif macro_name[1:] == 'F':
                        macro_pieces = [str(PurePath(x).name) for x in macro_pieces]

                    macro_tokens = TokenString.text(' '.join(macro_pieces))
                else:
                    if this_token.name in self._macros:
                        _, macro_tokens = self._macros[this_token.name]
                    else:
                        self._warn(f'warning: undefined macro {this_token.name}')
                        macro_tokens = TokenString.text('')
                macro_value = self.expand_macros(macro_tokens, current_target)
                if this_token.replacement is not None:
                    replaced, replacement = (self.expand_macros(t, current_target) for t in this_token.replacement)
                    macro_value = re.sub(re.escape(replaced) + r'\b', replacement, macro_value)
                return macro_value
            else:
                raise TypeError('unexpected token type!')

        return ''.join(expand_one(t) for t in text)

    def special_target(self, name: str) -> Optional['Target']:
        return self._targets.get(name, None)

    def special_target_has_prereq(self, target_name: str, name: str) -> bool:
        target = self.special_target(target_name)
        if target is None:
            return False
        return len(target.prerequisites) == 0 or name in target.prerequisites

    def target(self, name: str) -> 'Target':
        # TODO implement .DEFAULT
        # it's not POSIXful, but GNU make will use inference rules for defined targets with no commands,
        follow_gnu = True # TODO implement .POSIX and scope it properly
        if name not in self._targets or (follow_gnu and len(self._targets[name].commands) == 0):
            # > When no target rule is found to update a target, the inference rules shall be checked. The suffix of
            # > the target (.s1) to be built...
            suffix = PurePath(name).suffix
            # > is compared to the list of suffixes specified by the .SUFFIXES special targets. If the .s1 suffix is
            # > found in .SUFFIXES...
            # (single-suffix rules apply to targets with no suffix so we just throw that in)
            if self.special_target_has_prereq('.SUFFIXES', suffix) or suffix == '':
                # > the inference rules shall be searched in the order defined...
                for rule in self._inference_rules:
                    # > for the first .s2.s1 rule...
                    if rule.s1 == suffix:
                        # > whose prerequisite file ($*.s2) exists.
                        prerequisite_path = PurePath(name).with_suffix(rule.s2)
                        if ImpurePath(prerequisite_path).exists():
                            if name in self._targets:
                                # we got here by following GNU
                                self._warn(f'warning: non-POSIX use of inference rule {rule.s1}{rule.s2} on explicit '
                                           f'target {name}')
                            self._targets[name] = Target(name, [str(prerequisite_path)], rule.commands)
                            break
        if name not in self._targets:
            # we tried inference, it didn't work
            # is there a default?
            default = self.special_target('.DEFAULT')
            if default is not None:
                self._targets[name] = Target(name, [], default.commands)
            else:
                # well, there's no rule available, and no default. does it already exist?
                if ImpurePath(name).exists():
                    # it counts as already up to date
                    self._targets[name] = Target(name, [], [], True)
        return self._targets[name]

@dataclass()
class InferenceRule:
    s1: str # empty string means single-suffix rule
    s2: str
    commands: List['CommandLine']

    def __str__(self) -> str:
        return '\n'.join([
            f'{self.s1}{self.s2}:',
            *[f'\t{x}' for x in self.commands],
        ])

@dataclass()
class Target:
    name: str
    prerequisites: List[str]
    commands: List['CommandLine']
    already_updated: bool = False

    def __str__(self) -> str:
        return '\n'.join([
            f'{self.name}: {" ".join(self.prerequisites)}',
            *[f'\t{x}' for x in self.commands],
        ])

    def _path(self) -> ImpurePath:
        return ImpurePath(self.name)

    def modified_time(self) -> Optional[float]:
        path = self._path()
        if path.exists():
            return path.stat().st_mtime
        else:
            return None

    def newer_than(self, other: 'Target') -> Optional[bool]:
        self_mtime = self.modified_time()
        other_mtime = other.modified_time()
        if self_mtime is not None and other_mtime is not None:
            return self_mtime >= other_mtime
        elif self_mtime is None and self.already_updated and self.name in other.prerequisites:
            return True
        elif other_mtime is None and other.already_updated and other.name in self.prerequisites:
            return False
        else:
            return None

    def is_up_to_date(self, file: Makefile) -> bool:
        if self.already_updated:
            return True
        exists = self._path().exists()
        newer_than_all_dependencies = all(self.newer_than(file.target(other)) for other in self.prerequisites)
        return exists and newer_than_all_dependencies

    def update(self, file: Makefile) -> None:
        for prerequisite in self.prerequisites:
            file.target(prerequisite).update(file)
        if not self.is_up_to_date(file):
            self.execute_commands(file)
        self.already_updated = True

    def execute_commands(self, file: Makefile) -> None:
        for command in self.commands:
            command.execute(file, self)

@dataclass()
class MacroSource(enum.Enum):
    File = 0
    CommandLine = 1
    MAKEFLAGS = 2
    Environment = 3
    Builtin = 4

@dataclass()
class CommandLine:
    ignore_errors: bool
    silent: bool
    always_execute: bool
    execution_line: TokenString

    def __init__(self, line: TokenString):
        self.ignore_errors = False
        self.silent = False
        self.always_execute = False

        # POSIX:
        # > An execution line is built from the command line by removing any prefix characters.
        tokens_iter = iter(line)
        first_token = next(tokens_iter)
        if isinstance(first_token, TextToken):
            while len(first_token.text) > 0 and first_token.text[0] in ['-', '@', '+']:
                if first_token.text[0] == '-':
                    self.ignore_errors = True
                elif first_token.text[0] == '@':
                    self.silent = True
                elif first_token.text[0] == '+':
                    self.always_execute = True
                first_token.text = first_token.text[1:]
        self.execution_line = TokenString(list((first_token, *tokens_iter)))

    def __str__(self) -> str:
        return ''.join([
            '-' if self.ignore_errors else '',
            '@' if self.silent else '',
            '+' if self.always_execute else '',
            str(self.execution_line).replace('\n', '↵\n')
        ])

    def execute(self, file: Makefile, current_target: 'Target') -> None:
        # POSIX:
        # > If the command prefix contains a <hyphen-minus>, or the -i option is present, or the special target .IGNORE
        # > has either the current target as a prerequisite or has no prerequisites, any error found while executing
        # > the command shall be ignored.
        ignore_errors = self.ignore_errors or \
                        file.args.ignore_errors or \
                        file.special_target_has_prereq('.IGNORE', current_target.name)

        # > If the command prefix contains an at-sign and the make utility command line -n option is not specified, or
        # > the -s option is present, or the special target .SILENT has either the current target as a prerequisite or
        # > has no prerequisites, the command shall not be written to standard output before it is executed.
        silent = self.silent and not file.args.dry_run or \
                 file.args.silent or \
                 file.special_target_has_prereq('.SILENT', current_target.name)

        execution_line = file.expand_macros(self.execution_line, current_target)

        # > Except as described under the at-sign prefix...
        if not silent:
            # > the execution line shall be written to the standard output.
            print(execution_line)

        # > If the command prefix contains a <plus-sign>, this indicates a makefile command line that shall be executed
        # > even if -n, -q, or -t is specified.
        should_execute = self.always_execute or not (file.args.dry_run or file.args.question or file.args.touch)
        if not should_execute:
            return

        # > The execution line shall then be executed by a shell as if it were passed as the argument to the system()
        # > interface, except that if errors are not being ignored then the shell -e option shall also be in effect.
        # TODO figure out how to pass -e to the shell reliably
        result = subprocess.call(execution_line, shell=True)

        # > By default, when make receives a non-zero status from the execution of a command, it shall terminate with
        # > an error message to standard error.
        if not ignore_errors and result != 0:
            print('error!', file=sys.stderr)
            # TODO implement keep-going
            sys.exit(1)

BUILTIN_INFERENCE_RULES = [
    InferenceRule('', '.c', [CommandLine(tokenize('$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $<'))]),
    InferenceRule('', '.f', [CommandLine(tokenize('$(FC) $(FFLAGS) $(LDFLAGS) -o $@ $<'))]),
    InferenceRule('', '.sh', [
        CommandLine(tokenize('cp $< $@')),
        CommandLine(tokenize('chmod a+x $@'))
    ]),

    InferenceRule('.o', '.c', [CommandLine(tokenize('$(CC) $(CFLAGS) -c $<'))]),
    InferenceRule('.o', '.f', [CommandLine(tokenize('$(FC) $(FFLAGS) -c $<'))]),
    InferenceRule('.o', '.y', [
        CommandLine(tokenize('$(YACC) $(YFLAGS) $<')),
        CommandLine(tokenize('$(CC) $(CFLAGS) -c y.tab.c')),
        CommandLine(tokenize('rm -f y.tab.c')),
        CommandLine(tokenize('mv y.tab.o $@')),
    ]),
    InferenceRule('.o', '.l', [
        CommandLine(tokenize('$(LEX) $(LFLAGS) $<')),
        CommandLine(tokenize('$(CC) $(CFLAGS) -c lex.yy.c')),
        CommandLine(tokenize('rm -f lex.yy.c')),
        CommandLine(tokenize('mv lex.yy.o $@')),
    ]),
    InferenceRule('.c', '.y', [
        CommandLine(tokenize('$(YACC) $(YFLAGS) $<')),
        CommandLine(tokenize('mv y.tab.c $@')),
    ]),
    InferenceRule('.c', '.l', [
        CommandLine(tokenize('$(LEX) $(LFLAGS) $<')),
        CommandLine(tokenize('mv lex.yy.c $@')),
    ]),
    InferenceRule('.a', '.c', [
        CommandLine(tokenize('$(CC) -c $(CFLAGS) $<')),
        CommandLine(tokenize('$(AR) $(ARFLAGS) $@ $*.o')),
        CommandLine(tokenize('rm -f $*.o')),
    ]),
    InferenceRule('.a', '.f', [
        CommandLine(tokenize('$(FC) -c $(FFLAGS) $<')),
        CommandLine(tokenize('$(AR) $(ARFLAGS) $@ $*.o')),
        CommandLine(tokenize('rm -f $*.o')),
    ]),
]
BUILTIN_MACROS: Dict[str, Union[str, TokenString]] = {
    'MAKE': 'make',
    'AR': 'ar',
    #'ARFLAGS': '-rv',
    'YACC': 'yacc',
    'YFLAGS': '',
    'LEX': 'lex',
    'LFLAGS': '',
    'LDFLAGS': '',
    #'CC': 'c99',
    'CFLAGS': '-O 1',
    #'FC': 'fort77',
    'FFLAGS': '-O 1',

    # TODO bitch about the non-POSIXness of these GNUisms
    # from https://www.gnu.org/software/make/manual/html_node/Implicit-Variables.html#Implicit-Variables
    'AS': 'as',
    'CC': 'cc',
    'CXX': 'g++',
    'CPP': tokenize('$(CC) -E'),
    'FC': 'f77',
    'M2C': 'm2c',
    'PC': 'pc',
    'CO': 'co',
    'GET': 'get',
    'LINT': 'lint',
    'MAKEINFO': 'makeinfo',
    'TEX': 'tex',
    'TEXI2DVI': 'texi2dvi',
    'WEAVE': 'weave',
    'CWEAVE': 'cweave',
    'TANGLE': 'tangle',
    'CTANGLE': 'ctangle',
    'RM': 'rm -f',

    'ARFLAGS': 'rv',
}
BUILTIN_TARGETS = [
    Target('.SUFFIXES', ['.o', '.c', '.y', '.l', '.a', '.sh', '.f'], []),
]
