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
      
        ##
        ## simulation running GUI controls
        ##
        historicalLayout = QtGui.QHBoxLayout()

        self.startDate = QtGui.QDateEdit()
        self.startDate.setDateRange(QtCore.QDate(1990,1,1),QtCore.QDate.currentDate())
        self.startDate.setCalendarPopup(True)
        self.startDate.dateChanged.connect(self.set_start)
        
        self.endDate = QtGui.QDateEdit()
        self.endDate.setDateRange(QtCore.QDate(1990,1,1),QtCore.QDate.currentDate())
        self.endDate.setCalendarPopup(True)
        self.endDate.dateChanged.connect(self.set_end)
                
        go = QtGui.QPushButton('Run')
        go.clicked.connect(self.run_historical)
        historical = QtGui.QLabel('Run Historical')
        
        historicalLayout.addWidget(historical)
        historicalLayout.addWidget(self.startDate)
        historicalLayout.addWidget(self.endDate)
        historicalLayout.addWidget(go)

        realtimeLayout = QtGui.QHBoxLayout()
        realtime = QtGui.QLabel('Run Realtime')
        start = QtGui.QPushButton('Start')
        stop = QtGui.QPushButton('Stop')
        start.clicked.connect(self.run_test3)
        stop.clicked.connect(self.stop_realtime)
        
        realtimeLayout.addWidget(realtime)
        realtimeLayout.addWidget(start)
        realtimeLayout.addWidget(stop)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        mainLayout.addLayout(historicalLayout)
        mainLayout.addLayout(realtimeLayout)
        
        self.setLayout(mainLayout)


        self.setAcceptDrops(True)
        self.setWindowTitle("TradeUp")
    
    def set_start(self):
        """ sets start"""
        date = self.startDate.date()
        d = int(date.day())
        m = int(date.month())
        y = int(date.year())
        self.start = datetime.date(y,m,d)
        
        
    def set_end(self):
        """ sets end"""
        date = self.end.date()
        d = int(date.day())
        m = int(date.month())
        y = int(date.year())
        self.end = datetime.date(y,m,d)
        
    def run_historical(self):
        self.controller.run_historical(self.start, self.end)
        
    def run_realtime(self):
        self.controller.run_realtime()
    def stop_realtime(self):
        self.controller.stop_realtime()
        
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
