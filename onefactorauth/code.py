import re
import sys
from typing import Optional

import requests

from onefactorauth.config import get_config


def dump_passcode(timeout=10) -> int:
    passcode = get_passcode(timeout)
    if passcode is None:
        print("Err: no passcode found", file=sys.stderr)
        return 1

    print(passcode)
    return 0


def get_passcode(timeout=10) -> Optional[str]:
    conf = get_config()

    if conf is None:
        return

    s = requests.Session()

    # it needs to first set some cookies before we get latest sms
    s.get(__get_sms_url(conf.phone))

    r = s.get(__get_sms_url(conf.phone))
    return __parse_passcode(r.text, re.compile(r"SMS p\*\*\*codes: (\d+)"))


def __parse_passcode(html: str, passcode_pattern: re.Pattern) -> Optional[str]:
    passcodes = re.findall(passcode_pattern, html)
    if not passcodes:
        return
    return passcodes[0]


def __get_sms_url(phone: str) -> str:
    return f"https://receivesms.cc/sms/{phone}"
