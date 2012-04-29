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
from backend import Parser,Recipe 
from PySide.QtGui import *
from SimpleTable import AddButton,Table

class GraphTable(QtGui.QWidget):
    
    def __init__(self, frame,controller):
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
        
def Testing():
    
#{ name_of_recipe: [(a,b)...], other_recipe: [(a,b)...]} <-- where a*b is the thing you want to graph
    testingDates1 = [datetime.date(2006, 1, 3), datetime.date(2006, 1, 4),datetime.date(2006, 1, 5),datetime.date(2006, 1, 6),datetime.date(2006, 1, 7)]
    testingValue1 = [1,2,3,10,7]
    testingDates2 = [datetime.date(2006, 1, 5), datetime.date(2006, 1, 6),datetime.date(2006, 1, 7),datetime.date(2006, 1, 8),datetime.date(2006, 1, 9)]
    testingValue2 = [10,20,30,15,7]
    
    graph.makeLine('Test Profile 1',testingDates1,testingValue1,'b')
    graph.makeLine('Test Profile 2',testingDates2,testingValue2,'r')
    print graph.linedict
       
    frame = GraphUI.MainWindow()
    ex = GraphTable(frame)
    
    graph.addPoint('Test Profile 1', datetime.date(2006, 1, 8), 12)
    print graph.linedict


def main():
    
    app = QtGui.QApplication(sys.argv)
#{ name_of_recipe: [(a,b)...], other_recipe: [(a,b)...]} <-- where a*b is the thing you want to graph
    testingDates1 = [datetime.date(2006, 1, 3), datetime.date(2006, 1, 4),datetime.date(2006, 1, 5),datetime.date(2006, 1, 6),datetime.date(2006, 1, 7)]
    testingValue1 = [1,2,3,10,7]
    testingDates2 = [datetime.date(2006, 1, 5), datetime.date(2006, 1, 6),datetime.date(2006, 1, 7),datetime.date(2006, 1, 8),datetime.date(2006, 1, 9)]
    testingValue2 = [10,20,30,15,7]
    
    graph.makeLine('Test Profile 1',testingDates1,testingValue1,'b')
    graph.makeLine('Test Profile 2',testingDates2,testingValue2,'r')
    print graph.linedict
       
    frame = GraphUI.MainWindow()
    ex = GraphTable(frame)
    
    graph.addPoint('Test Profile 1', datetime.date(2006, 1, 8), 12)
    print graph.linedict
    #frame.reDraw()
    #ex.reDraw(frame.reDraw())
    #ex2 = GUI(frame)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

#sys.exit(app.exec_())