#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys

# Importamos los módulos de Qt
from PyQt4 import QtCore, QtGui, uic, Qt

# JSON para guardar la lista de contactos a disco
import json

#Modulo que permite el envío de mensajes
from personal import Personal


def _loadContactos(self):
    "Carga la lista de contactos de disco"
    try:
        f = open(os.path.expanduser('~/.contactos'))
        data = f.read()
        f.close()
        self.contactos = json.loads(data)
    except:
        self.contactos = []

    if self.contactos is None:
        # El archivo estaba vacío
        self.contactos = []


class Main(QtGui.QDialog):
    """La ventana principal de la aplicación."""
    def __init__(self):
        QtGui.QDialog.__init__(self)

        # Cargamos la interfaz desde el archivo .ui
        uifile = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), 'sms.ui')
        uic.loadUi(uifile, self)

        self.loadContactos()
        self.listContactos()

        self.personal = Personal()
        self.show_captcha()

        self.mensaje_text.setFocus()
        self.validation()

    loadContactos = _loadContactos

    '''Metodos para manejar lista de contactos'''
    def saveContactos(self):
        "Guarda las contactos a disco"
        f = open(os.path.expanduser('~/.contactos'), 'w')
        f.write(json.dumps(self.contactos))
        f.close()

    def listContactos(self):
        "Muestra las contactos en la lista"
        self.contactoList.clear()
        for nombre, url in self.contactos:
            self.contactoList.addItem(nombre)

    @QtCore.pyqtSlot()
    def on_add_clicked(self):
        addDlg = AddContacto(self)
        r = addDlg.exec_()
        if r:  # O sea, apretaron "Add"
            self.contactos.append((unicode(addDlg.name.text()),
                                    unicode(addDlg.number.text())))
            self.saveContactos()
            self.listContactos()

    @QtCore.pyqtSlot()
    def on_edit_clicked(self):
        "Edita el contacto actualmente seleccionado"
        curIdx = self.contactoList.currentRow()
        name, number = self.contactos[curIdx]
        editDlg = EditContacto(self)
        editDlg.name.setText(name)
        editDlg.number.setText(number)
        r = editDlg.exec_()
        if r:  # O sea, apretaron "Save"
            self.contactos[curIdx] = [unicode(editDlg.name.text()),
                                 unicode(editDlg.number.text())]
            self.saveContactos()
            self.listContactos()
            self.contactoList.setCurrentRow(curIdx)

    @QtCore.pyqtSlot()
    def on_remove_clicked(self):
        "Borra el contacto actualmente seleccionado"
        curIdx = self.contactoList.currentRow()
        del (self.contactos[curIdx])
        self.saveContactos()
        self.listContactos()

    def on_contactoList_clicked(self):
        curIdx = self.contactoList.currentRow()
        name, number = self.contactos[curIdx]
        self.number_entry.setText(number)
        if self.mensaje_text.toPlainText():
            if self.sender_entry.text():
                if self.captcha_entry.text():
                    self.send.setFocus()
                else:
                    self.captcha_entry.setFocus()
            else:
                self.sender_entry.setFocus()
        else:
            self.mensaje_text.setFocus()

    '''Metodos para enviar el mensaje'''
    def validation(self):
        self.number_entry.setMaxLength(10)
        self.captcha_entry.setMaxLength(4)
        re = QtCore.QRegExp('^[0-9]*$')
        validator = QtGui.QRegExpValidator(re, None)
        self.captcha_entry.setValidator(validator)
        self.number_entry.setValidator(validator)

    @QtCore.pyqtSlot()
    def renew_captcha(self):
        self.show_captcha()
        self.captcha_entry.clear()
        self.captcha_entry.setFocus()

    @QtCore.pyqtSlot()
    def clean_all(self):
        self.mensaje_text.clear()
        self.captcha_entry.clear()
        self.mensaje_text.setFocus()
        self.show_captcha()

    @QtCore.pyqtSlot()
    def show_captcha(self):
        imagenpath = self.personal.get_captcha()
        imagen = Qt.QPixmap(imagenpath)
        self.captcha.setPixmap(imagen)

    @QtCore.pyqtSlot()
    def send_sms(self):
        mensaje = self.mensaje_text.toPlainText()
        mensaje = unicode(mensaje)
        remitente = self.sender_entry.text()
        remitente = unicode(remitente)
        numero = self.number_entry.text()
        if numero.length() != 10:
            QtGui.QMessageBox.warning(self, u'Error', u'Número incorrecto')
            return 2
        captcha = self.captcha_entry.text()

        if self.personal.send(numero, captcha, mensaje, remitente):
            return 0
        else:
            return 1

    @QtCore.pyqtSlot()
    def on_send_clicked(self):
        answer = self.send_sms()
        if not answer:
            self.clean_all()
        elif answer == 1:
            QtGui.QMessageBox.warning(self, u'Error', u'Captcha incorrecto')
            self.renew_captcha()
        else:
            self.number_entry.setFocus()


class AddContacto(QtGui.QDialog):
    '''El dialogo de agregar un contacto'''
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)

        #Cargamos la interfaz desde el archivo ui
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),
            'contact.ui')
        uic.loadUi(uifile, self)


class EditContacto(AddContacto):
    '''El diálogo de editar un contacto.
    Es exactamente igual a Addcontacto, excepto
    que cambia el texto de un botón.
    '''
    def __init__(self, parent):
        AddContacto.__init__(self, parent)
        self.addButton.setText('Guardar')


def main():
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
