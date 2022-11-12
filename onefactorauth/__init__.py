import re
import sys
from argparse import ArgumentParser

from onefactorauth.code import ParseConf, dump_passcode
from onefactorauth.config import configure, dump_config


def main():
    parser = ArgumentParser(description="One factor authentication.")
    commands = parser.add_subparsers(dest="command", help="subcommand")

    config_parser = commands.add_parser("config", description="Configure 1fa")
    config_parser.add_argument(
        "-p",
        "--phone",
        help="phone number to use from https://receivesms.cc/sms/",
        type=str,
    )

    code_parser = commands.add_parser("code", description="Get 1fa code")
    code_parser.add_argument(
        "-c", "--clipboard", help="copy to clipboard", action="store_true"
    )
    code_parser.add_argument(
        "-t", "--timeout", help="timeout (s)", type=int, default=10
    )
    code_parser.add_argument(
        "-p",
        "--pattern",
        help="regex pattern for passcode",
        type=re.compile,
        default=re.compile("SMS p\*\*\*codes: (\d+)"),  # pattern for UCLA duo
    )
    code_parser.add_argument(
        "-m",
        "--max-time",
        help="maximum age of the sms code msg (min)",
        type=int,
        default=2,
    )

    args = parser.parse_args()

    if args.command == "config":
        if args.phone is None:
            return dump_config()
        return configure(args.phone)

    if args.command == "code":
        return dump_passcode(
            ParseConf(
                **{k: v for k, v in args.__dict__.items() if k in ParseConf._fields}
            ),
            args.clipboard,
        )

    print(
        "Err: Please provide a subcommand to run, run --help for more info",
        file=sys.stderr,
    )
    return 1
