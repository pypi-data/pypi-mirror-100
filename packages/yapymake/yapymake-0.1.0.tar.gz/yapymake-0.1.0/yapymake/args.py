import argparse
from dataclasses import dataclass
import os
import sys
from typing import List, Optional, TextIO

from . import DESCRIPTION, VERSION

__all__ = [
    'parse',
    'Args',
]

parser = argparse.ArgumentParser(
    description=f'{DESCRIPTION} - version {VERSION}',
)

parser.add_argument('--environment-overrides', '-e',
                    action='store_true',
                    help='Cause environment variables, including those with null values, to override macro assignments '
                         'within makefiles.')
parser.add_argument('--makefile', '--file', '-f',
                    action='append',
                    type=argparse.FileType('r'),
                    help="Specify a different makefile (or '-' for standard input).")
parser.add_argument('--ignore-errors', '-i',
                    action='store_true',
                    help='Ignore error codes returned by invoked commands.')
parser.add_argument('--keep-going', '-k',
                    action='store_true',
                    help='Continue to update other targets that do not depend on the current target if a non-ignored '
                         'error occurs while executing the commands to bring a target up-to-date.')
parser.add_argument('--dry-run', '--just-print', '--recon', '-n',
                    action='store_true',
                    help="Write commands that would be executed on standard output, but do not execute them (but "
                         "execute lines starting with '+').")
parser.add_argument('--print-everything', '--print-data-base', '-p',
                    action='store_true',
                    help='Write to standard output the complete set of macro definitions and target descriptions.')
parser.add_argument('--question', '-q',
                    action='store_true',
                    help='Return a zero exit value if the target file is up-to-date; otherwise, return an exit value '
                         'of 1.')
parser.add_argument('--no-builtin-rules', '-r',
                    action='store_false',
                    dest='builtin_rules',
                    help='Clear the suffix list and do not use the built-in rules.')
parser.add_argument('--no-keep-going', '--stop', '-S',
                    action='store_false',
                    dest='keep_going',
                    help='Terminate make if an error occurs while executing the commands to bring a target up-to-date '
                         '(default behavior, required by POSIX to be also a flag for some reason).')
parser.add_argument('--silent', '--quiet', '-s',
                    action='store_true',
                    help='Do not write makefile command lines or touch messages to standard output before executing.')
parser.add_argument('--touch', '-t',
                    action='store_true',
                    help='Update the modification time of each target as though a touch target had been executed.')
parser.add_argument('targets_or_macros',
                    nargs='*',
                    metavar='target_or_macro',
                    help='Target name or macro definition.')

@dataclass()
class Args:
    environment_overrides: bool
    makefile: List[TextIO]
    ignore_errors: bool
    keep_going: bool
    dry_run: bool
    print_everything: bool
    question: bool
    builtin_rules: bool
    silent: bool
    touch: bool
    targets_or_macros: List[str]

    def __init__(self, parsed_args: argparse.Namespace):
        self.environment_overrides = parsed_args.environment_overrides
        if parsed_args.makefile is not None and len(parsed_args.makefile) > 0:
            self.makefile = parsed_args.makefile
        else:
            try:
                self.makefile = [open('./makefile', 'r')]
            except FileNotFoundError:
                self.makefile = [open('./Makefile', 'r')]
        self.ignore_errors = parsed_args.ignore_errors
        self.keep_going = parsed_args.keep_going
        self.dry_run = parsed_args.dry_run
        self.print_everything = parsed_args.print_everything
        self.question = parsed_args.question
        self.builtin_rules = parsed_args.builtin_rules
        self.silent = parsed_args.silent
        self.touch = parsed_args.touch
        self.targets_or_macros = parsed_args.targets_or_macros

def parse(cli_args: Optional[List[str]] = None, env_makeflags: Optional[str] = None) -> Args:
    if cli_args is None:
        real_cli_args = sys.argv[1:]
    else:
        real_cli_args = cli_args
    if env_makeflags is None:
        real_env_makeflags = os.environ.get('MAKEFLAGS', '')
    else:
        real_env_makeflags = env_makeflags

    # per POSIX, we accept option letters without a leading -, so to simplify we prepend a - now
    # TODO allow macro definitions in MAKEFLAGS
    if len(real_env_makeflags) > 0 and not real_env_makeflags.startswith('-'):
        real_env_makeflags = '-' + real_env_makeflags

    if len(real_env_makeflags) > 0:
        all_args = [real_env_makeflags, *real_cli_args]
    else:
        all_args = real_cli_args

    return Args(parser.parse_args(all_args))

# TODO test any of this
