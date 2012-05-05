'''
Created on Mar 14, 2012

@author: WillIV
'''
#!/usr/bin/python
# -*- coding: utf-8 -*-

# simple.py
import sys
import GraphUI
import graph
import datetime
from PySide import QtGui, QtCore
from PySide.QtCore import *
from backend import Parser,Recipe , Controller
from PySide.QtGui import *
from SimpleTable import AddButton,Table


class GraphTable(QtGui.QWidget):
    
    def __init__(self, frame, controller):
        super(GraphTable, self).__init__()
        self.controller = controller 
        self.initUI(frame)
        
    def initUI(self,frame):      

        hbox = QtGui.QHBoxLayout(self)   
        # set a controller for the table/graph
        bottom = QtGui.QFrame(self)
        bottom.setFrameShape(QtGui.QFrame.StyledPanel)
        self.table = Table()
        # set the table's controller
        self.table.controller = self.controller 
        addButton = AddButton(self.table)
        buttonTable = QVBoxLayout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(addButton)
        bottom.setLayout(layout)

        

        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(frame)
        splitter.addWidget(bottom)  

        hbox.addWidget(splitter)
        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
       
        self.setGeometry(300, 300, 700, 600)
        self.setWindowTitle('TradeUp')
        self.show()
        
    def reDraw(self,frame):
        hbox = QtGui.QHBoxLayout(self)   

        bottom = QtGui.QFrame(self)
        bottom.setFrameShape(QtGui.QFrame.StyledPanel)

        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(frame)
        splitter.addWidget(bottom)

        hbox.addWidget(splitter)
        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
        self.setGeometry(300, 300, 700, 600)
        self.setWindowTitle('TradeUp')
        self.show()