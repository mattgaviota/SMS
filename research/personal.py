#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from debug import debug
from decoradores import Verbose, Retry
from browser import get_browser
#from random import randrange
import webbrowser
import re
import sys
import os

FORMURL = """http://sms2.personal.com.ar/Mensajes/sms.php"""


@Retry(10)
def show_captcha():
    browser = get_browser()
    html = browser.get_html(FORMURL)
    match = re.search(r'"(http://.*?tmp/.*?\.png)"', html)
    if match:
        return webbrowser.open(match.group(1))


def send():
    
    browser = get_browser()
    while True:

        captcha = show_captcha()
        form = browser.get_forms()[0]
        form.set_all_readonly(False)


        form["Snb"] = '3875174708'
        form["codigo"] = raw_input('captcha: ')
        form["msgtext"] = 'mensaje prueba' + '-' + 'remitente'
        form["FormValidar"] = "validar"

        form.submit()
