#!/usr/bin/env python
#-*- coding: utf-8 -*-

import Tkinter as tk
from PIL import Image, ImageTk
import personal

class App:

    def __init__(self, master):

        self.frame = tk.Frame(master)
        self.frame.grid()
        self.remitente = tk.StringVar()
        self.codarea = tk.StringVar()
        self.numlocal = tk.StringVar()
        self.mensaje = ''
        imagen = Image.open("captcha.png")
        self.photo = ImageTk.PhotoImage(imagen)
        self.lenmax = 110 - len(self.remitente.get())
        
        '''Boton para salir'''
        self.button = tk.Button(self.frame, text="Salir", command=self.frame.quit)
        self.button.grid(row = 2, column = 6)
        
        '''Boton para enviar'''
        self.hi_there = tk.Button(self.frame, text="Enviar", command=self.send)
        self.hi_there.grid(row = 2, column = 5)
        
        '''Etiqueta del remitente'''
        self.remitente_label = tk.Label(self.frame, text = "Remitente")
        self.remitente_label.grid(row = 1, column = 1)
        
        '''Caja de entrada para el remitente'''
        self.ent_remitente = tk.Entry(self.frame, width = 10, textvariable = self.remitente)
        self.ent_remitente.grid(row = 1, column = 2)
        
        '''Etiqueta del codigo de area'''
        self.cod_label = tk.Label(self.frame, text = "Codigo de area")
        self.cod_label.grid(row = 1, column = 3)
        
        '''Caja de entrada del codigo de area'''
        self.ent_codarea = tk.Entry(self.frame, width = 4, textvariable = self.codarea)
        self.ent_codarea.grid(row = 1, column = 4)
        
        '''Etiqueta del numero local'''
        self.num_label = tk.Label(self.frame, text = "Numero")
        self.num_label.grid(row = 1, column = 5)
        
        '''Caja de entrada para el numero local'''
        self.ent_numlocal = tk.Entry(self.frame, width = 7, textvariable = self.numlocal)
        self.ent_numlocal.grid(row = 1, column = 6)
        
        '''Etiqueta del mensaje'''
        self.msje_label = tk.Label(self.frame, text = "Mensaje")
        self.msje_label.grid(row = 2, column = 3)
        
        self.ent_msje = tk.Text(self.frame, width=20, height=4)
        self.ent_msje.grid(row = 2, column = 4) 
        
        '''Etiqueta del captcha'''
        self.cap_label = tk.Label(self.frame, text = "Captcha")
        self.cap_label.grid(row = 2, column = 1)
        
        '''Imagen del captcha'''
        self.captcha_label = tk.Label(self.frame, image = self.photo)
        self.captcha_label.photo = self.photo
        self.captcha_label.grid(row = 2, column = 2)
        
    def send(self):
        self.mensaje =  self.ent_msje.get("1.0", tk.END)
        print self.mensaje

def main():
    root = tk.Tk()
    root.title("SMS to Personal")
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
