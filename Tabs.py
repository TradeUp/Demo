#!/usr/bin/env python

import sys
import GraphTable
import GraphUI
import graph
import datetime
#from GraphTable import Testing
from PySide import QtGui, QtCore
from PySide.QtCore import *
from backend import Parser,Recipe , Controller
from PySide.QtGui import *
from SimpleTable import AddButton,Table
import DragAndDrop
import time


class Tabs(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

#        testingDates1 = [datetime.date(2006, 1, 3), datetime.date(2006, 1, 4),datetime.date(2006, 1, 5),datetime.date(2006, 1, 6),datetime.date(2006, 1, 7)]
#        testingValue1 = [1,2,3,10,7]
#        testingDates2 = [datetime.date(2006, 1, 5), datetime.date(2006, 1, 6),datetime.date(2006, 1, 7),datetime.date(2006, 1, 8),datetime.date(2006, 1, 9)]
#        testingValue2 = [10,20,30,15,7]
#    
#        graph.makeLine('Test Profile 1',testingDates1,testingValue1,'b')
#        graph.makeLine('Test Profile 2',testingDates2,testingValue2,'r')
#        print graph.linedict
       
        frame = GraphUI.MainWindow()
        self.controller = Controller(None,None)
        ex = GraphTable.GraphTable(frame,self.controller)
        # set the graph too
        self.controller.table = ex.table 
        frame.controller = self.controller
        # now the frame is the graph (i.e. has the method makenew)
        self.controller.graph = frame
        

        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(ex,"Graph")
        tabWidget.addTab(DragAndDrop.RecipeWindow(), "Kitchen") 
      
        TestButton = QtGui.QPushButton("TestMe")
#        cancelButton = QtGui.QPushButton(self.tr("Cancel"))
        print "hello" 
        TestButton.clicked.connect(self.run_test3);
        print "hello3"
#        self.connect(TestButton, QtCore.SIGNAL("clicked()"), self, Tabs.run_test3(self))
#        self.connect(cancelButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("reject()"))

        buttonLayout = QtGui.QHBoxLayout()
#        buttonLayout.addStretch(1)
        buttonLayout.addWidget(TestButton)
#        buttonLayout.addWidget(cancelButton)
#        recipeParser = Parser('test.algo')
#        self.controller.portfolio = recipeParser.build_portfolio()
#        for recipe in self.controller.portfolio.recipes.values():
#            self.controller.graphed.append(recipe.name)
#            self.controller.table.addRecipe(recipe.name)
#        self.controller.run(1)
        print "hello4"
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)


        self.setAcceptDrops(True)
        self.setWindowTitle("TradeUp")
    
    #@QtCore.SLOT()
    def run_test3(self):
        print 'building new parser/portfolio from test.algo'
        recipeParser = Parser('test.algo')
        self.controller.portfolio = recipeParser.build_portfolio()
        for recipe in self.controller.portfolio.recipes.values():
            self.controller.graphed.append(recipe.name)
            self.controller.table.addRecipe(recipe.name)
        # run the controller evaluating in a loop
        print "Test called"
        for x in xrange(1,20):
            self.controller.run(x) # every other one should be true (xing fingers)
            #time.sleep(.5)

class GeneralTab(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        fileNameLabel = QtGui.QLabel("Drag and Drop goes here")
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(fileNameLabel)

        mainLayout.addStretch(1)
        self.setLayout(mainLayout)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    tabdialog = Tabs()
    sys.exit(tabdialog.exec_())
