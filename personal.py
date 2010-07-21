#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import browser
from decoradores import Verbose
import re

@Verbose(2)
def main():
    binstance = browser.BROWSER()
    binstance.go("http://sms1.personal.com.ar/Mensajes/sms.php")
    form = binstance.get_forms()[0]

    match = re.search(r'"(http://.*?tmp/.*?\.png)"', binstance.get_html())
    if match:
        browser.webbrowser.open(match.group(1))

    captcha = raw_input("Captcha: ")

    while True:
        form["CODAREA"] = raw_input("Códido de área: ")
        form["NRO"] = raw_input("Número: ")
        form["DE_MESG_TXT"] = raw_input("Remitente: ")
        form["MESG_TXT"] = raw_input("Mensaje: ")
        form["codigo"] = captcha
        form.submit()
        binstance.show()

if __name__ == "__main__":
    exit(main())

