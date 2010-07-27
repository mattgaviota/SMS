#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from debug import debug
from decoradores import Verbose
from pprint import pprint
from browser import BROWSER
import webbrowser
import re



def controla_mensaje(longremitente):
    longmaxima = 110 - longremitente
    mensaje = raw_input('mensaje (le quedan %d caracteres) : ' %(longmaxima,)) 
    bandera = 1
    while (len(mensaje) >= longmaxima) and bandera:
        mensaje = mensaje[:longmaxima]
        print 'su mensaje es el siguiente :'
        print mensaje
        print 'su mensaje fue acortado por superar el limite de caracteres'
        print 'desea reescribirlo? (y/n)'
        opcion = raw_input('respuesta : ')
        if opcion in ['y','Y']:
            mensaje = raw_input('mensaje (le quedan %d caracteres) : '
                 %(longmaxima,))
        else:
            print 'su mensaje sera enviado como fue recortado'
            bandera = 0
    return mensaje

@Verbose(2)
def main():
    browser = BROWSER()
    form = browser.get_forms("http://sms1.personal.com.ar/Mensajes/sms.php")[0]

    match = re.search(r'"(http://.*?tmp/.*?\.png)"', browser.get_html())
    if match:
        webbrowser.open(match.group(1))

    print(form)

    print("Datos de la sessión:")
    form["codigo"] = raw_input("  Captcha(verifique su navegador): ")
    form["CODAREA"] = raw_input("  Códido de área: ")
    form["NRO"] = raw_input("  Número: ")
    form["DE_MESG_TXT"] = raw_input("  Remitente: ")

    print("Mensajes: (deje en blanco para salir)")
    while True:
        mensaje = controla_mensaje(len(form["DE_MESG_TXT"]))
        if not mensaje:
            debug("Saliendo limpiamente xD")
            return

        form["MESG_TXT"] = mensaje
        print("  enviando...")
        form.submit()

if __name__ == "__main__":
    exit(main())

