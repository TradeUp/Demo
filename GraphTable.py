#!/usr/bin/python

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
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(addButton)
        addIcon = QtGui.QPixmap('add.png')
        addButton.setIcon(addIcon)
        addButton.setFixedSize(60,32)
        ### add the progress bar
        progress = QtGui.QProgressBar()
        progress.setAlignment(QtCore.Qt.AlignLeft)
        progress.setVisible(False)
        self.controller.progress = progress
        progress.setValue(0)
        layout.addWidget(progress)
        bottom.setLayout(layout)

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
        start_icon = QtGui.QPixmap('play.png')
        start.setIcon(start_icon)
        stop_icon = QtGui.QPixmap('stop.png')
        go.setIcon(start_icon)
        stop = QtGui.QPushButton('Stop')
        stop.setIcon(stop_icon)
        start.setFixedWidth(100)
        stop.setFixedWidth(100)
        go.setFixedWidth(100)
        start.clicked.connect(self.run_realtime)
        stop.clicked.connect(self.stop_realtime)
        
        realtimeLayout.addWidget(realtime)
        realtimeLayout.addWidget(start)
        realtimeLayout.addWidget(stop)


        layout.addLayout(historicalLayout)
        layout.addLayout(realtimeLayout)

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
     