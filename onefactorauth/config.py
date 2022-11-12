from contextlib import suppress
from pathlib import Path
from typing import NamedTuple, Optional

import yaml

home = Path.home()
secrets = home / ".secrets.yml"


class Config(NamedTuple):
    phone: str


def configure(phone: str) -> int:
    conf = Config(phone=phone)
    existing = __read_config()

    entry = __get_onefa_entry(existing)

    # create an empty entry if no existing entry
    if entry is None:
        entry = {"app": "onefa", "env": []}
        existing.append(entry)

    # turn conf into a list of { "name": string, "value": string }
    entry["env"] = [{"name": k, "value": v} for k, v in conf._asdict().items()]

    __write_config(existing)

    return 0


def dump_config() -> int:
    conf = get_config()

    if conf is None:
        print("No configuration yet :(")
        return 1

    print("Configuration")
    for key, value in conf._asdict().items():
        print(key, value)

    return 0


def get_config() -> Optional[Config]:
    all_config = __read_config()

    conf = __get_onefa_entry(all_config)
    if conf is None:
        return

    with suppress(Exception):
        return Config(**{var["name"]: var["value"] for var in conf["env"]})


def __read_config():
    with suppress(FileNotFoundError):
        with open(secrets, "r") as fin:
            return yaml.safe_load(fin)

    return []


def __write_config(config):
    with open(secrets, "w+") as fout:
        yaml.dump(config, fout)


def __get_onefa_entry(config):
    for conf in config:
        if conf.get("app") == "onefa":
            return conf
