#!/usr/bin/env python
#-*- coding: utf-8 -*-

import Tkinter as tk
import re
import urllib

from PIL import Image, ImageTk
from browser import get_browser
from codecs import decode, encode
from debug import debug
from decoradores import Verbose, Retry
from random import randrange
from tkMessageBox import showinfo, showerror

FORMURL = """http://sms2.personal.com.ar/Mensajes/sms.php"""

#TODO Agregar contactos


class Main_app:

    def __init__(self, master):

        self.main_frame = tk.Frame(master, bg='#c8c8c8')
        self.main_frame.grid(ipadx=2, ipady=2, padx=2, pady=2)
        self.remitente = tk.StringVar()
        self.codarea = tk.StringVar()
        self.numlocal = tk.StringVar()
        self.captcha = tk.StringVar()
        self.lenmax = 110 - len(self.remitente.get())
        self.browser = get_browser()

        self.show_captcha()

        '''Etiqueta del número'''
        self.cod_label = tk.Label(self.main_frame, text="Número de destino",
            bg='#c8c8c8')
        self.cod_label.grid(row=1, column=1, sticky=tk.W)

        '''Caja de entrada del número'''
        self.ent_codarea = tk.Entry(self.main_frame, width=10,
            textvariable=self.codarea, bd=2, relief=tk.GROOVE)
        self.ent_codarea.grid(row=1, column=2, sticky=tk.W + tk.E)
        self.ent_codarea.focus_set()

        '''Etiquetas de ejemplo de número'''
        self.ejemplo_label = tk.Label(self.main_frame,
            text="código de area sin el 0\n y el número sin el 15",
            bg='#c8c8c8')
        self.ejemplo_label.grid(row=2, column=1, sticky=tk.N)

        self.ejemplo_label = tk.Label(self.main_frame,
            text="por ejemplo\n 3874567890", bg='#c8c8c8')
        self.ejemplo_label.grid(row=2, column=2, sticky=tk.N)

        '''Etiqueta del remitente'''
        self.remitente_label = tk.Label(self.main_frame, text="Tu Nombre",
            bg='#c8c8c8')
        self.remitente_label.grid(row=1, column=3, sticky=tk.E)

        '''Caja de entrada para el remitente'''
        self.ent_remitente = tk.Entry(self.main_frame, width=10,
            textvariable=self.remitente, bd=2, relief=tk.GROOVE)
        self.ent_remitente.grid(row=1, column=4, sticky=tk.W + tk.E)

        '''Etiqueta del mensaje'''
        self.msje_label = tk.Label(self.main_frame, text="Mensaje",
            bg='#c8c8c8')
        self.msje_label.grid(row=2, column=3, sticky=tk.W)

        '''Entrada de texto para el mensaje'''
        self.ent_msje = tk.Text(self.main_frame, width=25, height=4,
            wrap="word", bd=2, relief=tk.GROOVE)
        self.ent_msje.grid(row=2, column=4)
        self.ent_msje.bind("<KP_Enter>", self.keypress_return)

        '''Etiqueta del captcha'''
        self.cap_label = tk.Label(self.main_frame,
            text="Palabra de verificación", bg='#c8c8c8')
        self.cap_label.grid(row=3, column=1, sticky=tk.E)

        '''Caja de entrada para el captcha'''
        self.ent_captcha = tk.Entry(self.main_frame, width=4,
            textvariable=self.captcha, bd=2, relief=tk.GROOVE)
        self.ent_captcha.grid(row=3, column=3, sticky=tk.W)
        self.ent_captcha.bind("<Return>", self.keypress_return)
        self.ent_captcha.bind("<KP_Enter>", self.keypress_return)

        '''Boton para enviar'''
        self.hi_there = tk.Button(self.main_frame, text="Enviar",
            command=self.send, relief=tk.FLAT, bg='#c8c8c8', bd=0)
        self.hi_there.grid(row=3, column=4)

    def keypress_return(self, event):
        self.send()

    def comprobar_cadena(self, cadena, longitud):
        for caracter in cadena:
            if caracter in '0123456789':
                pass
            else:
                return False

        if len(cadena) == longitud:
            return True
        else:
            return False

    def send(self):
        mensaje = self.ent_msje.get("1.0", tk.END)
        codarea = self.codarea.get()
        if not self.comprobar_cadena(codarea, 10):
            message = 'Número incorrecto, debe tener 10 números'
            showerror(title='Error', message=message)
            return 0
        numlocal = self.numlocal.get()
        remitente = self.remitente.get()
        captcha = self.captcha.get()
        if not self.comprobar_cadena(captcha, 4):
            message = 'Captcha incorrecto, debe tener 4 números'
            showerror(title='Error', message=message)
            return 0
        self.sendsms(remitente, codarea, numlocal, mensaje, captcha)
        self.clean()
        return 0

    def clean(self):
        self.captcha.set('')
        self.ent_msje.delete("1.0", tk.END)
        self.ent_msje.focus_set()
        self.show_captcha()
        return 0

    def show_captcha(self):
        html = self.browser.get_html(FORMURL)
        match = re.search(r'(http://.*?tmp/.*?\.png)', html)

        while (type(match) == type(None)) or (not match.group()):
            html = browser.get_html(FORMURL)
            match = re.search(r'(http://.*?tmp/.*?\.png)', html)

        imageurl = match.group()
        imagepath = r'/tmp/captchalive.png'
        urllib.urlretrieve(imageurl, imagepath)
        imagen = Image.open(imagepath)
        self.photo = ImageTk.PhotoImage(imagen)

        '''Imagen del captcha'''
        self.captcha_label = tk.Label(self.main_frame, image=self.photo, bd=0)
        self.captcha_label.photo = self.photo
        self.captcha_label.grid(row=3, column=2, sticky=tk.W)
        return 0

    def sendsms(self, remitente, codarea, numlocal, mensaje, captcha):
        form = self.browser.get_forms()[0]
        form.set_all_readonly(False)
        mensaje = encode(mensaje, 'latin-1', 'replace')

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
        return 0


def main():
    root = tk.Tk()
    root.title("SMS to Personal")
    app = Main_app(root)
    root.mainloop()
    return 0

if __name__ == '__main__':
    main()
