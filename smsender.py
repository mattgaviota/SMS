#!/usr/bin/env python
#-*- coding: utf-8 -*-

import Tkinter as tk
from PIL import Image, ImageTk
from debug import debug
from decoradores import Verbose, Retry
from browser import get_browser
from random import randrange
import re
import urllib

FORMURL = """http://sms2.personal.com.ar/Mensajes/sms.php"""

class App:

    def __init__(self, master):

        self.frame = tk.Frame(master, bg = '#c8c8c8')
        self.frame.grid()
        self.remitente = tk.StringVar()
        self.codarea = tk.StringVar()
        self.numlocal = tk.StringVar()
        self.captcha = tk.StringVar()
        self.lenmax = 110 - len(self.remitente.get())
        
        
        self.show_captcha()
        
        
        '''Etiqueta del codigo de area'''
        self.cod_label = tk.Label(self.frame, text = "Codigo de area",
            bg = '#c8c8c8')
        self.cod_label.grid(row = 1, column = 1, sticky = tk.E)
        
        '''Caja de entrada del codigo de area'''
        self.ent_codarea = tk.Entry(self.frame, width = 4, 
            textvariable = self.codarea, bd = 2)
        self.ent_codarea.grid(row = 1, column = 2, sticky = tk.W)
        
        '''Etiqueta del numero local'''
        self.num_label = tk.Label(self.frame, text = "Numero", bg = '#c8c8c8')
        self.num_label.grid(row = 1, column = 3, sticky = tk.W)
        
        '''Caja de entrada para el numero local'''
        self.ent_numlocal = tk.Entry(self.frame, width = 7, 
            textvariable = self.numlocal, bd = 2)
        self.ent_numlocal.grid(row = 1, column = 4, sticky = tk.W)
        
        '''Etiqueta del remitente'''
        self.remitente_label = tk.Label(self.frame, text = "De",
            bg = '#c8c8c8')
        self.remitente_label.grid(row = 2, column = 1, sticky = tk.E)
        
        '''Caja de entrada para el remitente'''
        self.ent_remitente = tk.Entry(self.frame, width = 10, 
            textvariable = self.remitente, bd = 2)
        self.ent_remitente.grid(row = 2, column = 2, sticky = tk.W + tk.E)
        
        
        '''Etiqueta del mensaje'''
        self.msje_label = tk.Label(self.frame, text = "Mensaje", 
            bg = '#c8c8c8')
        self.msje_label.grid(row = 2, column = 3, sticky = tk.W)
        
        '''Entrada de texto para el mensaje'''
        self.ent_msje = tk.Text(self.frame, width=25, height=4, wrap = "word",
            bd = 2)
        self.ent_msje.grid(row = 2, column = 4)
        self.ent_msje.bind("<KP_Enter>", self.keypress_return)
        
        '''Etiqueta del captcha'''
        self.cap_label = tk.Label(self.frame, text = "Captcha", bg = '#c8c8c8')
        self.cap_label.grid(row = 3, column = 1, sticky = tk.E)
        
        '''Caja de entrada para el captcha'''
        self.ent_captcha = tk.Entry(self.frame, width = 4,
            textvariable = self.captcha, bd =  2)
        self.ent_captcha.grid(row = 3, column = 3, sticky = tk.W)
        self.ent_captcha.bind("<Return>", self.keypress_return)
        self.ent_captcha.bind("<KP_Enter>", self.keypress_return)
        
        '''Boton para enviar'''
        self.hi_there = tk.Button(self.frame, text="Enviar", command=self.send,
            relief = tk.FLAT, bg = '#c8c8c8', bd = 0)
        self.hi_there.grid(row = 3, column = 4)

    def keypress_return(self, event):
        self.send()
                
    def send(self):
        mensaje =  self.ent_msje.get("1.0", tk.END)
        codarea = self.codarea.get()
        numlocal = self.numlocal.get()
        remitente = self.remitente.get()
        captcha = self.captcha.get()
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
        browser = get_browser()
        html = browser.get_html(FORMURL)
        match = re.search(r'(http://.*?tmp/.*?\.png)', html)
        
        while ( not match.group() ) or ( match == None ):
            html = browser.get_html(FORMURL)
            match = re.search(r'(http://.*?tmp/.*?\.png)', html)
            
        imageurl = match.group()
        imagepath = r'/tmp/captchalive.png'
        urllib.urlretrieve(imageurl, imagepath)
        imagen = Image.open(imagepath)
        self.photo = ImageTk.PhotoImage(imagen)
        '''Imagen del captcha'''
        self.captcha_label = tk.Label(self.frame, image = self.photo, bd = 0)
        self.captcha_label.photo = self.photo
        self.captcha_label.grid(row = 3, column = 2, sticky = tk.W)
        return 0

    def sendsms(self, remitente, codarea, numlocal, mensaje, captcha):
        browser = get_browser()
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
        return 0
        
def main():
    root = tk.Tk()
    root.title("SMS to Personal")
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
