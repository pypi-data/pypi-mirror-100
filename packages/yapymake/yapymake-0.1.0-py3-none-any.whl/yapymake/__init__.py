VERSION = '0.1.0'
DESCRIPTION = 'A (mostly) POSIX-compatible make implemented in Python'

from .args import parse
from .makefile import Makefile

def main() -> None:
    these_args = parse()
    file = Makefile(these_args)
    # TODO dump command line into MAKEFLAGS
    # TODO dump command line macros into environment
    # TODO handle SHELL
    for input_file in these_args.makefile:
        file.read(input_file)

    targets = [arg for arg in these_args.targets_or_macros if '=' not in arg]
    if len(targets) == 0:
        assert file.first_non_special_target is not None
        targets = [file.first_non_special_target]

    if these_args.print_everything:
        print(file)

    for target in targets:
        file.target(target).update(file)
