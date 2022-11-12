import sys

import setuptools

# Thank you @KentoNishi for this setup.py

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except:
    long_description = "A tool to bypass 2 factor authentication."

try:
    with open("requirements.txt", "r") as reqs:
        requirements = reqs.read().split("\n")
except:
    requirements = ""

try:
    if "refs/tags/v" in sys.argv[1]:
        versionName = sys.argv[1].replace("refs/tags/v", "")
        del sys.argv[1]
    else:
        raise Exception
except:
    versionName = "0.1.0"

setuptools.setup(
    name="onefactorauth",
    version=versionName,
    author="Ronak Badhe",
    author_email="ronak.badhe@gmail.com",
    description=long_description.split("\n")[1],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/r2dev2/onefactorauth",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "onefactorauth=onefactorauth:main",
            "1fa=onefactorauth:main",
        ]
    },
    python_requires=">=3.5",
    install_requires=requirements,
)
