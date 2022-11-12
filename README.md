# OneFactorAuth

A tool to bypass 2 factor authentication.

## Usage

### Installation

```sh
python3 -m pip install onefactorauth
```

### Setup

1. Go to https://receivesms.cc/sms/ and choose a phone number
2. Run `1fa config -p <phone_number>` (ex: `1fa config -p <31616099881>`)
3. Register the phone number under your account for 2 factor authentication
4. Go to https://receivesms.cc/sms/<phone_number> (ex: `https://receivesms.cc/sms/31616099881`) to see the text message
5. Complete the setup of this phone number in your account settings
6. Take note of the pattern of the message, eg. how it is structured, where the code is

### Invoking

```
$: 1fa code --help

usage: 1fa code [-h] [-c] [-t TIMEOUT] [-p PATTERN] [-m MAX_TIME]

Get 1fa code

options:
  -h, --help            show this help message and exit
  -c, --clipboard       copy to clipboard
  -t TIMEOUT, --timeout TIMEOUT
                        timeout (s)
  -p PATTERN, --pattern PATTERN
                        regex pattern for passcode
  -m MAX_TIME, --max-time MAX_TIME
                        maximum age of the sms code msg (min)
```

* pattern for the passcode should have one capture group with the code
    * ex: messages are like `SMS p***codes: 93209`
        * pattern of `SMS p\*\*\*codes: (\d+)`
    * ex: messages are like `Your Uber code is 43890`
        * pattern of `Uber code is (\d+)` (partial matches are acceptable
* bind `1fa code --pattern='code is (\d+)' --clipboard` to a keybind
    * windows: use [winhotkey](https://directedge.us/content/winhotkey/)
    * macos: [automator or icanhazshortcut](https://www.howtogeek.com/286332/how-to-run-any-mac-terminal-command-with-a-keyboard-shortcut/)
    * linux: depends on your desktop environment, there's something in the built in settings for gnome and xfce

## How

It uses https://receivesms.cc/sms/ to receive and scrape texts for your text passcode

## Why

UCLA makes me 2fa every time I wanna log into my portal. No one's trying to hack my BruinBill, UCLA, just lemme use my account. I have 2fa setup for GitHub and Discord which are likelier targets for hacking and neither of them ask me for 2fa on every login.


## License

Do WTF You Want To Public License

## Developers

Developed by [Ronak Badhe (r2dev2)](https://github.com/r2dev2)
