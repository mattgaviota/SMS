#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import re
import urllib

from codecs import encode

from browser import get_browser


class Personal():

    def __init__(self):
        self.browser = get_browser()
        self.path = "http://sms2.personal.com.ar/Mensajes/sms.php"

    def get_captcha(self):
        '''
        Obtiene una imagen que contiene un captcha desde la pagina de
        personal. La guarda en un archivo temporal y retorna el path
        hacia la imagen.
        '''
        html = self.browser.get_html(self.path)
        match = re.search(r'(http://.*?tmp/.*?\.png)', html)

        while (type(match) == type(None)) or (not match.group()):
            html = self.browser.get_html(self.path)
            match = re.search(r'(http://.*?tmp/.*?\.png)', html)

        imageurl = match.group()
        imagepath = r'/tmp/captchalive.png'
        urllib.urlretrieve(imageurl, imagepath)
        return imagepath

    def send(self, number, captcha, message, sender):
        '''
        Rellena un formulario con los parametros y lo envia a la pagina de
        personal, para que esta haga el envío.
        Si el envío se realiza con exito devuelve True, en otro caso False.
        '''
        form = self.browser.get_forms()[0]
        form.set_all_readonly(False)
        message = message + u'-' + sender
        message = encode(message, 'latin-1', 'replace')

        form["Snb"] = number
        form["codigo"] = captcha
        form["msgtext"] = message
        form["FormValidar"] = "validar"

        form.submit()

        error_message = '/home/smsonline/fallidos'
        if error_message in self.browser.get_html():
            return False
        else:
            return True
