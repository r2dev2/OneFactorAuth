import re
import sys
import time
from typing import Optional

import clipboard as clip
import requests

from onefactorauth.config import get_config


def dump_passcode(timeout=10, clipboard=False) -> int:
    passcode = get_passcode(timeout)
    if passcode is None:
        print("Err: no passcode found", file=sys.stderr)
        return 1

    print(passcode)
    if clipboard:
        clip.copy(passcode)

    return 0


def get_passcode(timeout=10) -> Optional[str]:
    start = time.time()
    conf = get_config()

    if conf is None:
        return

    s = requests.Session()

    # it needs to first set some cookies before we get latest sms
    s.get(__get_sms_url(conf.phone))

    while time.time() - start <= timeout:
        r = s.get(__get_sms_url(conf.phone))
        code = __parse_passcode(r.text, re.compile(r"SMS p\*\*\*codes: (\d+)"))
        if code is not None:
            return code


def __parse_passcode(html: str, passcode_pattern: re.Pattern) -> Optional[str]:
    passcodes = re.findall(passcode_pattern, html)
    if not passcodes:
        return
    return passcodes[0]


def __get_sms_url(phone: str) -> str:
    return f"https://receivesms.cc/sms/{phone}"
