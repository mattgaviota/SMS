#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from debug import debug
from decoradores import Verbose
import browser
import re

@Verbose(2)
def main():
    binstance = browser.BROWSER()
    binstance.go("http://sms1.personal.com.ar/Mensajes/sms.php")
    form = binstance.get_forms()[0]

    match = re.search(r'"(http://.*?tmp/.*?\.png)"', binstance.get_html())
    if match:
        browser.webbrowser.open(match.group(1))

    print("Datos de la sessión:")
    form["codigo"] = raw_input("  Captcha: ")
    form["CODAREA"] = raw_input("  Códido de área: ")
    form["NRO"] = raw_input("  Número: ")
    form["DE_MESG_TXT"] = raw_input("  Remitente: ")

    print("Mensajes: (deje en blanco para salir)")
    while True:
        mensaje = raw_input("  Nuevo mensaje: ")
        if not mensaje:
            debug("Saliendo limpiamente xD")
            return

        form["MESG_TXT"] = mensaje
        print("  enviando...")
        form.submit()

if __name__ == "__main__":
    exit(main())

