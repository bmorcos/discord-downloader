#!/usr/bin/env python

import io

try:
    from setuptools import find_packages, setup
except ImportError:
    raise ImportError(
        "'setuptools' is required but not installed. To install it, "
        "follow the instructions at "
        "https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py"
    )


def read(*filenames, **kwargs):
    encoding = kwargs.get("encoding", "utf-8")
    sep = kwargs.get("sep", "\n")
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


install_req = ["discord"]

setup(
    name="discord-downloader",
    version="0.0.1",
    author="Ben Morcos",
    author_email="morcos.ben@gmail.com",
    packages=find_packages(),
    description="Simple bot to download files from Discord",
    long_description=read("README.md"),
    install_requires=install_req,
    python_requires=">=3.6",
)
