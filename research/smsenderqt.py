#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys

# Importamos los módulos de Qt
from PyQt4 import QtCore, QtGui, uic

# JSON para guardar la lista de contactos a disco
import json


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
        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'sms.ui')
        uic.loadUi(uifile, self)

        self.loadContactos()
        self.listContactos()

    loadContactos = _loadContactos

    def saveContactos(self):
        "Guarda las contactos a disco"
        f = open(os.path.expanduser('~/.contactos'),'w')
        f.write(json.dumps(self.contactos))
        f.close()

    def listContactos(self):
        "Muestra las contactos en la lista"
        self.contactoList.clear()
        for nombre,url in self.contactos:
            self.contactoList.addItem(nombre)

    @QtCore.pyqtSlot()
    def on_add_clicked(self):
        addDlg = AddContacto(self)
        r = addDlg.exec_()
        if r: # O sea, apretaron "Add"
            self.contactos.append ((unicode(addDlg.name.text()),
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
        if r: # O sea, apretaron "Save"
            self.contactos[curIdx]= [unicode(editDlg.name.text()),
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

class AddContacto(QtGui.QDialog):
    '''El dialogo de agregar un contacto'''
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)

        #Cargamos la interfaz desde el archivo ui
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),
            'contact.ui')
        uic.loadUi(uifile, self)


class EditContacto(AddContacto):
    """El diálogo de editar un contacto.
    Es exactamente igual a Addcontacto, excepto
    que cambia el texto de un botón."""
    def __init__(self, parent):
        AddContacto.__init__(self, parent)
        self.addButton.setText("guardar")


def main():
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
