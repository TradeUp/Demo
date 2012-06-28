'''
Created on Apr 14, 2012

@author: Paavan
'''
import PySide
import sys
from PySide import QtCore
from PySide import QtGui
from Function import *
import string

class Inspector(QtGui.QFrame):
    def __init__(self, controller):
        super(Inspector, self).__init__();
        
        #default message.
        lblEmpty = QtGui.QLabel("No function selected.");
        
        layout = QtGui.QVBoxLayout();
        layout.addWidget(lblEmpty);
        
        layout.setContentsMargins(0,0,0,0);
        
        self.controller = controller
        self.setLayout(layout);
        
    '''Set the editor for this inspector, given a function object'''
    @QtCore.Slot(object)
    def setEditor(self, func):
        print "SETTING EDITOR FOR FUNCTION"
        if not func:
            layout = self.layout()
            w = layout.takeAt(0)
            w.widget().deleteLater()
            layout.addWidget(QtGui.QLabel("No function selected."))
            self.setLayout(layout)
        elif isinstance(func, SimpleFunction):
            layout = self.layout()
            w = layout.takeAt(0)
            w.widget().deleteLater();
            layout.addWidget(SimpleEditor(func, self.controller))
            self.setLayout(layout)
        elif isinstance(func, TechnicalFunction):
            layout = self.layout()
            w = layout.takeAt(0)
            w.widget().deleteLater()
            layout.addWidget(TechnicalEditor(func, self.controller))
            self.setLayout(layout)
        elif(isinstance(func, DummyFunction)):
            layout = self.layout()
            w = layout.takeAt(0)
            w.widget().deleteLater();
            layout.addWidget(DummyEditor(func))
            self.setLayout(layout)
        

class Editor(QtGui.QWidget):
    def __init__(self):
        super(Editor, self).__init__()

"""
Editor for a SimpleFunction object
"""
class TechnicalEditor(Editor):
    def __init__(self, func, controller):
        super(TechnicalEditor, self).__init__()
        
        self.controller = controller
        
        self.func = func;
        rootVLayout = QtGui.QVBoxLayout()
        
        layoutRow1 = QtGui.QHBoxLayout()
        layoutRow2 = QtGui.QHBoxLayout()

        labelA = QtGui.QLabel("Stock A: ")
        labelA.setMaximumHeight(45)
        
        labelB = QtGui.QLabel("Stock B: ")
        labelB.setMaximumHeight(45)
        btnSave = QtGui.QPushButton("Save")
        
        btnSave.clicked.connect(self.updateFunc)
        
        self.txtStockA = QtGui.QLineEdit()
        self.txtStockA.setMaximumHeight(25)
        
        self.txtStockA.setText(func.stockA());
        
        self.txtStockB = QtGui.QLineEdit()
        self.txtStockB.setMaximumHeight(25)
        
        self.txtStockB.setText(func.stockB());
        
        self.txtStockB.textChanged.connect(self.resetTextEdit);
        
        layoutRow1.addWidget(labelA)
        layoutRow1.addWidget(self.txtStockA)
        
        layoutRow2.addWidget(labelB)
        layoutRow2.addWidget(self.txtStockB)
        
        rootVLayout.addLayout(layoutRow1); 
        rootVLayout.addLayout(layoutRow2)
        rootVLayout.addWidget(btnSave);  
        self.setLayout(rootVLayout);
        
    @QtCore.Slot()
    def updateFunc(self):
        tickerA = string.upper(self.txtStockA.text())
        tickerB = string.upper(self.txtStockB.text())
        if(self.controller.validate_ticker(tickerA)):
            self.txtStockA.setStyleSheet("background-color:#00FF00;");
            self.func.setStockA(tickerA)
            self.func.setAValid(True)
        else:
            self.txtStockA.setStyleSheet("background-color:#FF0000;");
            self.func.setAValid(False)
        if(self.controller.validate_ticker(tickerB)):
            self.txtStockB.setStyleSheet("background-color:#00FF00;");
            self.func.setStockB(tickerB)
            self.func.setBValid(True)
        else:
            self.txtStockB.setStyleSheet("background-color:#FF0000;");
            self.func.setBValid(False)
            
    @QtCore.Slot()
    def resetTextEdit(self):
        self.txtStockA.setStyleSheet("")
        self.txtStockB.setStyleSheet("")
        
    """
    Bind the enter key to saving
    """
    def keyPressEvent(self, event):
        self.updateFunc()
        
"""
Editor for a TechnicalFunction object
"""
class SimpleEditor(Editor):
    def __init__(self, func, controller):
        super(SimpleEditor, self).__init__()
        
        self.controller = controller
        
        self.func = func;
        rootVLayout = QtGui.QVBoxLayout()
        
        layout = QtGui.QHBoxLayout()
        label = QtGui.QLabel("Stock: ")
        label.setMaximumHeight(45)
        
        btnSave = QtGui.QPushButton("Save")
        
        btnSave.clicked.connect(self.updateFunc)
        
        self.txtStock = QtGui.QLineEdit()
        self.txtStock.setMaximumHeight(25)
        
        self.txtStock.setText(func.stock());
        
        self.txtStock.textChanged.connect(self.resetTextEdit);
        
        layout.addWidget(label)
        layout.addWidget(self.txtStock)
        
        rootVLayout.addLayout(layout); 
        rootVLayout.addWidget(btnSave);  
        self.setLayout(rootVLayout);
        
    @QtCore.Slot()
    def updateFunc(self):
        ticker = string.upper(self.txtStock.text())
        
        if(self.controller.validate_ticker(ticker)):
            self.txtStock.setStyleSheet("background-color:#00FF00;");
            self.func.setStock(ticker)
            self.func.setValid(True)
        else:
            self.txtStock.setStyleSheet("background-color:#FF0000;");
            self.func.setValid(False)
            
    @QtCore.Slot()
    def resetTextEdit(self):
        self.txtStock.setStyleSheet("");
        
    """
    Bind the enter key to saving
    """
    def keyPressEvent(self, event):
        self.updateFunc();
        
        
"""
Editor for a SimpleFunction object
"""
class DummyEditor(Editor):
    def __init__(self, func):
        super(DummyEditor, self).__init__()
        
        self.func = func;
        
        rootVLayout = QtGui.QVBoxLayout()
        
        layout = QtGui.QHBoxLayout()
        
        label = QtGui.QLabel("Value: ")
        label.setMaximumHeight(45)
        
        self.txtStock = QtGui.QTextEdit()
        self.txtStock.setMaximumHeight(25)
        self.txtStock.setText(str(func.value()))
        self.txtStock.textChanged.connect(self.updateFunc)
        
        layout.addWidget(label)
        layout.addWidget(self.txtStock)
        
        rootVLayout.addLayout(layout);
        
        self.setLayout(rootVLayout);
        
    @QtCore.Slot()
    def updateFunc(self):
        self.func.setValue(int(self.txtStock.text()))
        print "Updated func.stock to: " + self.txtStock.text()