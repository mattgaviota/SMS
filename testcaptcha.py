#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from debug import debug
import os
from pytesser import pytesser
import shutil
import Image


def resolver(path):
    result = pytesser.image_to_string(path)
    return result


def main():
    for path in os.listdir("captchas"):
        print("%s:%s" % (path, resolver(Image.open("captchas/%s" % path))))


if __name__ == "__main__":
    exit(main())
