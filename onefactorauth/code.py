import re
import sys
import time
from contextlib import suppress
from typing import NamedTuple, Optional

import clipboard as clip
import requests

from onefactorauth.config import get_config


class Passcode(NamedTuple):
    code: str
    time: int


class ParseConf(NamedTuple):
    pattern: re.Pattern
    timeout: int
    max_time: int


def dump_passcode(pconf: ParseConf, clipboard: bool) -> int:
    passcode = get_passcode(pconf)
    if passcode is None:
        print("Err: no passcode found", file=sys.stderr)
        return 1

    print(passcode)
    if clipboard:
        clip.copy(passcode)

    return 0


def get_passcode(pconf: ParseConf) -> Optional[str]:
    start = time.time()
    conf = get_config()

    if conf is None:
        return

    s = requests.Session()

    # it needs to first set some cookies before we get latest sms
    s.get(__get_sms_url(conf.phone))

    while time.time() - start <= pconf.timeout:
        r = s.get(__get_sms_url(conf.phone))
        code = __parse_passcode(r.text, pconf.pattern)
        if code is None:
            continue
        if code.time > pconf.max_time:
            return
        return code.code


def __parse_passcode(html: str, passcode_pattern: re.Pattern) -> Optional[Passcode]:
    passcodes = re.findall(passcode_pattern, html)
    if not passcodes:
        return
    timestamp = __parse_passcode_timestamp(html, passcodes[0])
    if not timestamp:
        return
    return Passcode(code=passcodes[0], time=timestamp)


def __parse_passcode_timestamp(html: str, code) -> Optional[int]:
    code_idx = html.find(code)
    date_start = html.rfind("<date>", 0, code_idx)
    date_end = html.rfind("</date>", 0, code_idx)
    if -1 in (date_start, date_end):
        return

    # <date> describes when sms was sent and can be in one of three formats
    # 1. (x minutes ago)
    # 2. (x seconds ago)
    # 3. () - means just sent
    date = html[date_start:date_end]
    minute_match = re.search(r"(\d+) minutes ago", date)
    if minute_match:
        return int(minute_match.group(1))

    # we return in minutes so no need to calculate exact time
    # for seconds and instant
    if "seconds ago" in date or "()" in date:
        return 0


def __get_sms_url(phone: str) -> str:
    return f"https://receivesms.cc/sms/{phone}"
