#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from browser import BROWSER
from decoradores import Verbose
import re

@Verbose(2)
def main():
    browser = BROWSER()
    browser.go("http://sms1.personal.com.ar/Mensajes/sms.php")
    form = browser.get_forms()[0]

    match = re.search(r'"(http://.*?tmp/.*?\.png)"', browser.get_html())
    if match:
        print match.group(1)

    captcha = raw_input("Captcha: ")

    while True:
        form["CODAREA"] = raw_input("Códido de área: ")
        form["NRO"] = raw_input("Número: ")
        form["DE_MESG_TXT"] = raw_input("Remitente: ")
        form["MESG_TXT"] = raw_input("Mensaje: ")
        form["codigo"] = captcha
        form.submit()
        browser.show()

if __name__ == "__main__":
    exit(main())

