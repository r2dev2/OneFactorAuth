import sys
from argparse import ArgumentParser

from onefactorauth.code import dump_passcode
from onefactorauth.config import configure, dump_config


def main():
    parser = ArgumentParser(description="One factor authentication.")
    commands = parser.add_subparsers(dest="command", help="subcommand")

    config_parser = commands.add_parser("config", description="Configure 1fa")
    config_parser.add_argument(
        "-p",
        "--phone",
        help="Phone number to use from https://receivesms.cc/sms/",
        type=str,
    )

    code_parser = commands.add_parser("code", description="Get 1fa code")

    args = parser.parse_args()

    if args.command == "config":
        if args.phone is None:
            return dump_config()
        return configure(args.phone)

    if args.command == "code":
        return dump_passcode()

    print(
        "Err: Please provide a subcommand to run, run --help for more info",
        file=sys.stderr,
    )
    return 1
