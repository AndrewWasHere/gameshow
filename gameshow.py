"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import argparse

from app.gameshow import make_gameshow


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--port',
        nargs='?',
        default=None,
        help='Port number'
    )
    return parser.parse_args()


def main():
    args = parse_command_line()
    app = make_gameshow()
    app.run(host='0.0.0.0', port=args.port)


if __name__ == '__main__':
    main()
