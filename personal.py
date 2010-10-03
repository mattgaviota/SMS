#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from debug import debug
from decoradores import Verbose, Retry
from browser import get_browser
from random import randrange
import webbrowser
import re
import sys
import os

FORMURL = """http://sms2.personal.com.ar/Mensajes/sms.php"""
COOKIESTORE = os.path.expanduser("""~/.personal.cookie""")

class Conversation(object):

    def __init__(self, remitente, destinatario):
        self.remitente = remitente
        self.destinatario = destinatario
        self.browser = get_browser()
        self._form = None


    @property
    def form(self, force=False):
        if force or self._form is None:
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
        mensaje = mensaje[:maxlen]
        print('Recortado a: %s' % mensaje)
        opcion = raw_input('Desea reescribirlo? (S/n): ')
        if opcion in ('s', 'S', 'y', 'Y', ' ', ''):
            mensaje = read_mensaje(remitente)
        else:
            print('Su mensaje será enviado como fue recortado')
            return mensaje.ljust(maxlen)

    return mensaje.ljust(maxlen)


@Retry(10)
def show_captcha():
    browser = get_browser()
    html = browser.get_html(FORMURL)
    match = re.search(r'"(http://.*?tmp/.*?\.png)"', html)
    if match:
        webbrowser.open(match.group(1))
#        debug("Captcha: %s" % match.group(1))
        return raw_input("  Captcha(verifique su navegador): ")



def main():
    browser = get_browser()

    browser.save_cookies(COOKIESTORE)

    if len(sys.argv) == 4:
        remitente, codarea, numlocal = sys.argv[1:]
    elif len(sys.argv) == 1:
        print("Datos de la sessión:")
        remitente = raw_input("  Remitente: ")
        codarea = raw_input("  Códido de área: ")
        numlocal = raw_input("  Número: ")
    else:
        print("Si no se pasa argumentos le seran preguntados sino invoque:")
        print("    %s remitente codarea numlocal" % sys.argv[0])
        return 1



    print("Mensajes: (deje en blanco para salir)")
    while True:

        # <WTF! No debería funcionar con el cookie incorrecto, ¿que no?>
        # R: Conserva la sesión, reemplaza el valor del captcha, bien diseñado
        # </WTF!>

        captcha = show_captcha()
        mensaje = read_mensaje(remitente)
        if not mensaje:
            debug("Saliendo limpiamente xD")
            return

        else:

            print("  enviando...")

            form = browser.get_forms()[0]
            form.set_all_readonly(False)

            form["CODAREA"] = codarea
            form["DE_MESG_TXT"] = remitente
            form["FormValidar"] = "validar"
            form["MESG_TXT"] = mensaje
            form["NRO"] = numlocal
            form["Snb"] = codarea + numlocal
            form["codigo"] = captcha
            form["msgtext"] = mensaje
            form["pantalla"] = "%s: %s - a %s%s" % (remitente, mensaje, codarea,
                numlocal)
            form["sig"] = remitente
            form["sizebox"] = str(110 - len(remitente) - len(mensaje))
            form["subname"] = codarea + numlocal

            form.submit(coord=(randrange(100), randrange(100)))

if __name__ == "__main__":
    exit(main())

