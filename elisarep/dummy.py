"""Simple script for debugging purposes

This script allows the user to try a simple script from external program.
It has similar args as the report generation script to try it out.
It creates a directory, and writes a file foo.txt there.
"""

from os import path, makedirs
import argparse


def main():
    """ Dummy test main
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "workdir", help="working directory of an experiment", default=None)
    parser.add_argument('--par', action='store_true',
                        help="use par files as input", default=False)

    args = parser.parse_args()
    working_dir = args.workdir
    par_input = args.par

    print('Testing scipt...')
    print(f'Working directory is `{working_dir}`')
    print('par input is set to `{par_input}`\n')

    new_dir = path.join(working_dir, '_foo_dir')
    makedirs(new_dir, exist_ok=True)

    try:
        new_file = path.join(new_dir, 'foo.txt')
        with open(new_file, 'w', encoding="utf-8") as fl:
            fl.write(f':)\npar is {par_input}\n')
    except (Exception,) as e:
        print('Error: ' + str(e))


if __name__ == "__main__":
    main()
