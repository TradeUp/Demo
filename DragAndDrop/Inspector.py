'''
Created on Apr 14, 2012

@author: Paavan
'''
import PySide
import sys
from PySide import QtCore
from PySide import QtGui
from Function import *

class Inspector(QtGui.QFrame):
    def __init__(self):
        super(Inspector, self).__init__();
        
        #default message.
        lblEmpty = QtGui.QLabel("No function selected.");
        
        layout = QtGui.QVBoxLayout();
        layout.addWidget(lblEmpty);
        
        layout.setContentsMargins(0,0,0,0);
        
        self.setLayout(layout);
        
    '''Set the editor for this inspector, given a function object'''
    @QtCore.Slot(object)
    def setEditor(self, func):
        print "SETTING EDITOR FOR FUNCTION"
        if(func == None):
            layout = self.layout()
            w = layout.takeAt(0)
            w.widget().deleteLater();
            layout.addWidget(QtGui.QLabel("No function selected."))
            self.setLayout(layout)
        elif(isinstance(func, SimpleFunction)):
            layout = self.layout()
            w = layout.takeAt(0)
            w.widget().deleteLater();
            layout.addWidget(SimpleEditor(func))
            self.setLayout(layout)

class Editor(QtGui.QWidget):
    def __init__(self):
        super(Editor, self).__init__()

"""
Editor for a SimpleFunction object
"""
class SimpleEditor(Editor):
    def __init__(self, func):
        super(SimpleEditor, self).__init__()
        
        self.func = func;
        
        rootVLayout = QtGui.QVBoxLayout()
        
        layout = QtGui.QHBoxLayout()
        
        label = QtGui.QLabel("Stock: ")
        label.setMaximumHeight(45)
        
        self.txtStock = QtGui.QTextEdit()
        self.txtStock.setMaximumHeight(25)
        self.txtStock.textChanged.connect(self.updateFunc)
        
        layout.addWidget(label)
        layout.addWidget(self.txtStock)
        
        rootVLayout.addLayout(layout);
        
        self.setLayout(rootVLayout);
        
    @QtCore.Slot()
    def updateFunc(self):
        self.func.setStock(self.txtStock.toPlainText())
        print "Updated func.stock to: " + self.txtStock.toPlainText()