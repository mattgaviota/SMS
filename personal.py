#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from debug import debug
from decoradores import Verbose
from browser import get_browser
from random import randrange
import webbrowser
import re
import sys
import os

FORMURL = """http://sms1.personal.com.ar/Mensajes/sms.php"""
COOKIESTORE = os.path.expanduser("""~/.personal.cookie""")

class Conversation(object):

    def __init__(self, remitente, destinatario):
        self.remitente = remitente
        self.destinatario = destinatario
        self.browser = get_browser()
        self._form = None


    @property
    def form(self):
        if self._form is None:
            self._form = self.browser.get_forms(FORMURL)[0]
        
        return self._form


    def send_sms(self, mensaje):
       """La función que hace el trabajo duro"""
       pass
       return



def read_mensaje(remitente):
    """Ayuda para recortar mensaje en interfaz de usuario en modo texto"""
    maxlen = 110 - len(remitente)
    mensaje = raw_input('mensaje (max %d caracteres): ' % maxlen)

    while (len(mensaje) > maxlen):
        mensaje = mensaje[:longmaxima]
        print('Recortado a: %s' % mensaje)
        opcion = raw_input('Desea reescribirlo? (s/n): ')
        if opcion in 'sSyY':
            mensaje = get_mensaje(remitente)
        else:
            print('Su mensaje será enviado como fue recortado')
            return mensaje

    return mensaje


def show_captcha(html):
    match = re.search(r'"(http://.*?tmp/.*?\.png)"', html)
    if match:
        webbrowser.open(match.group(1))
    else:
        debug("No se encontró captcha")
        browser.show()
        return 1



@Verbose(2)
def main():
    browser = get_browser()
    form = browser.get_forms(FORMURL)[0]
    form.set_all_readonly(False)
    print form

    browser.save_cookies(COOKIESTORE)

    if len(sys.argv) == 4:
        remitente, codarea, numlocal = sys.argv[1:]
    else:
        remitente = raw_input("  Remitente: ")
        codarea = raw_input("  Códido de área: ")
        numlocal = raw_input("  Número: ")

    print("Datos de la sessión:")

    show_captcha(browser.get_html())
    form["codigo"] = raw_input("  Captcha(verifique su navegador): ")

    form["FormValidar"] = "validar"
    form["CODAREA"] = codarea
    form["NRO"] = numlocal
    form["Snb"] = codarea + numlocal
    form["subname"] = codarea + numlocal
    form["DE_MESG_TXT"] = remitente
    form["sig"] = remitente

    print("Mensajes: (deje en blanco para salir)")
    while True:

#        show_captcha(browser.get_html())
#        form["codigo"] = raw_input("  Captcha(verifique su navegador): ")

        # <WTF! No debería funcionar con el cookie incorrecto, ¿que no?>
        browser.load_cookies(COOKIESTORE)
        # </WTF!>

        mensaje = read_mensaje(remitente)
        if not mensaje:
            debug("Saliendo limpiamente xD")
            return
        else:
            form["MESG_TXT"] = mensaje
            form["msgtext"] = mensaje
            form["pantalla"] = "%s: %s - a %s%s" % (remitente, mensaje, codarea,
                numlocal)
            form["sizebox"] = str(110 - len(remitente) - len(mensaje))
            print("  enviando...")
            form.submit(coord=(randrange(100), randrange(100)))

if __name__ == "__main__":
    exit(main())

