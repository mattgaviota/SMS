#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import re
import urllib

from codecs import encode

from browser import get_browser


class Personal():

    def __init__(self):
        self.browser = get_browser()
        self.path = """http://sms2.personal.com.ar/Mensajes/sms.php"""

    def get_captcha(self):
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

            form = self.browser.get_forms()[0]
            form.set_all_readonly(False)
            message = encode(message, 'latin-1', 'replace')

            form["Snb"] = number
            form["codigo"] = captcha
            form["msgtext"] = message + '-' + sender
            form["FormValidar"] = "validar"

            form.submit()
            return 0
