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
        self.start = None
        self.end = None 
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
        

        self.tabWidget = QtGui.QTabWidget()
        self.tabWidget.addTab(ex,"Graph")
        self.kitchen = DragAndDrop.RecipeWindow(self.controller)
        self.tabWidget.addTab(self.kitchen, "Kitchen") 
      
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
        start.clicked.connect(self.run_realtime)
        stop.clicked.connect(self.stop_realtime)
        
        realtimeLayout.addWidget(realtime)
        realtimeLayout.addWidget(start)
        realtimeLayout.addWidget(stop)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.tabWidget)
        mainLayout.addLayout(historicalLayout)
        mainLayout.addLayout(realtimeLayout)
        
        self.setLayout(mainLayout)


        self.setAcceptDrops(True)
        self.setWindowTitle("TradeUp")
    
    def addMenuItems(self, fileMenu):
        self.mnuSaveRecipe = QtGui.QAction('Save Recipe..', self)
        self.mnuSaveRecipe.setShortcut('Ctrl+S')
        self.mnuSaveRecipe.setStatusTip('Save the current recipe')
        self.mnuSaveRecipe.setEnabled(False)
        self.mnuSaveRecipe.setMenuRole(QtGui.QAction.MenuRole.ApplicationSpecificRole);
        self.mnuSaveRecipe.triggered.connect(self.kitchen.saveRecipe)
        
        self.mnuSavePortfolio = QtGui.QAction('Save Portfolio..', self)
        self.mnuSavePortfolio.setShortcut('Ctrl+S')
        self.mnuSavePortfolio.setStatusTip('Save the current portfolio')
        self.mnuSavePortfolio.setEnabled(True)
        self.mnuSavePortfolio.setMenuRole(QtGui.QAction.MenuRole.ApplicationSpecificRole);
        
        self.mnuSaveRecipeAs = QtGui.QAction('Save Recipe as..', self)
        self.mnuSaveRecipeAs.setStatusTip('Save the current recipe')
        self.mnuSaveRecipeAs.setEnabled(False)
        self.mnuSaveRecipeAs.setMenuRole(QtGui.QAction.MenuRole.ApplicationSpecificRole);
        self.mnuSaveRecipeAs.triggered.connect(self.kitchen.saveRecipeAs)
        
        self.mnuSavePortfolioAs = QtGui.QAction('Save Portfolio as..', self)
        self.mnuSavePortfolioAs.setStatusTip('Save the current portfolio')
        self.mnuSavePortfolioAs.setEnabled(True)
        self.mnuSavePortfolioAs.setMenuRole(QtGui.QAction.MenuRole.ApplicationSpecificRole);
        
        self.mnuOpenRecipe = QtGui.QAction('Open Recipe..', self)
        self.mnuOpenRecipe.setStatusTip('Open a recipe')
        self.mnuOpenRecipe.setEnabled(False)
        self.mnuOpenRecipe.setMenuRole(QtGui.QAction.MenuRole.ApplicationSpecificRole);
        self.mnuOpenRecipe.triggered.connect(self.kitchen.openRecipe)
        
        self.mnuOpenPortfolio = QtGui.QAction('Open Portfolio..', self)
        self.mnuOpenPortfolio.setStatusTip('Open a portfolio')
        self.mnuOpenPortfolio.setEnabled(True)
        self.mnuOpenPortfolio.setMenuRole(QtGui.QAction.MenuRole.ApplicationSpecificRole);
        
        fileMenu.addAction(self.mnuOpenRecipe)
        fileMenu.addAction(self.mnuOpenPortfolio)
        fileMenu.addAction(self.mnuSaveRecipe)
        fileMenu.addAction(self.mnuSaveRecipeAs)
        fileMenu.addAction(self.mnuSavePortfolio)
        fileMenu.addAction(self.mnuSavePortfolioAs)
        
        self.tabWidget.currentChanged.connect(self.tabChanged)
    
    def tabChanged(self, index):
        
        #make it easier to set all menu items to enabled or not, avoiding the need for huge if statements
        recipeMode = True
        if(index == 0): recipeMode = False
        
        self.mnuOpenPortfolio.setEnabled(not recipeMode)
        self.mnuSavePortfolio.setEnabled(not recipeMode)
        self.mnuSavePortfolioAs.setEnabled(not recipeMode)
        
        self.mnuOpenRecipe.setEnabled(recipeMode)
        self.mnuSaveRecipe.setEnabled(recipeMode)
        self.mnuSaveRecipeAs.setEnabled(recipeMode)
            
    
    def set_start(self):
        """ sets start"""
        date = self.startDate.date()
        d = int(date.day())
        m = int(date.month())
        y = int(date.year())
        self.start = datetime.date(y,m,d)
        
        
    def set_end(self):
        """ sets end"""
        date = self.endDate.date()
        d = int(date.day())
        m = int(date.month())
        y = int(date.year())
        self.end = datetime.date(y,m,d)
        
    def run_historical(self):
        if not self.start or self.end:
            self.set_start()
            self.set_end()
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
