#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from debug import debug
from decoradores import Verbose
from pprint import pprint
from browser import BROWSER
import webbrowser
import re


def get_mensaje(remitente):
    maxlen = 110 - len(remitente)
    mensaje = raw_input('mensaje (max %d caracteres) : ' % maxlen)

    while (len(mensaje) > maxlen):
        mensaje = mensaje[:longmaxima]
        print('Recortado a: %s' % mensaje)
        opcion = raw_input('Desea reescribirlo? (s/n): ')
        if opcion in 'sSyY':
            mensaje = get_mensaje(remitente)
        else:
            print('Su mensaje sera enviado como fue recortado')
            return mensaje

    return mensaje


@Verbose(2)
def main():
    browser = BROWSER()
    form = browser.get_forms("http://sms1.personal.com.ar/Mensajes/sms.php")[0]

    match = re.search(r'"(http://.*?tmp/.*?\.png)"', browser.get_html())
    if match:
        webbrowser.open(match.group(1))
    else:
        debug("No se encontró captcha")
        browser.show()
        return 1

    print(form)

    print("Datos de la sessión:")
    form["codigo"] = raw_input("  Captcha(verifique su navegador): ")
    form["CODAREA"] = raw_input("  Códido de área: ")
    form["NRO"] = raw_input("  Número: ")
    remitente = raw_input("  Remitente: ")
    form["DE_MESG_TXT"] = remitente

    print("Mensajes: (deje en blanco para salir)")
    while True:
        mensaje = get_mensaje(remitente)
        if not mensaje:
            debug("Saliendo limpiamente xD")
            return

        form["MESG_TXT"] = mensaje
        print("  enviando...")
        form.submit()

if __name__ == "__main__":
    exit(main())

