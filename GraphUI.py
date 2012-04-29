'''
Created on Mar 23, 2012

@author: WillIV
'''
import sys
import platform

import datetime
import numpy as np
import PySide
from PySide.QtGui import QApplication, QMainWindow, QTextEdit, QMessageBox, QWidget, QVBoxLayout
from PySide import QtCore

__version__ = '0.4.1'


import matplotlib

matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import graph
import matplotlib.font_manager as font_manager

class MainWindow(QMainWindow):

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        self.controller = None # this is set in tabs
        self.main_frame = QWidget()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent( self.main_frame )

        
        self.axes = self.figure.add_subplot(111)
        self.axes.grid(color='0.75', linestyle='-', linewidth=0.5)      
        for line in graph.linedict.items():
            self.axes.plot(line[1][0],line[1][1], color=line[1][2], label=line[0])
        props = font_manager.FontProperties(size=10)
        self.axes.legend(loc='center left', shadow=True, fancybox=True, prop=props)
        vbox = QVBoxLayout( )
        vbox.addWidget( self.canvas )
        self.main_frame.setLayout( vbox )
        self.setCentralWidget( self.main_frame )
        #self.canvas.draw()
        
    def reDraw(self):
        self.canvas.draw()
        
    def testing(self):
        print 'hi'

    def update(self,data,callback,table,table_data):
        graph.makenew(data)
        table.callback(table_data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    testingDates1 = [datetime.date(2006, 1, 3), datetime.date(2006, 1, 4),datetime.date(2006, 1, 5),datetime.date(2006, 1, 6),datetime.date(2006, 1, 7)]
    testingValue1 = [1,2,3,10,7]
    testingDates2 = [datetime.date(2006, 1, 5), datetime.date(2006, 1, 6),datetime.date(2006, 1, 7),datetime.date(2006, 1, 8),datetime.date(2006, 1, 9)]
    testingValue2 = [10,20,30,15,7]
    
    graph.makeLine('Test Profile 1',testingDates1,testingValue1,'b')
    graph.makeLine('Test Profile 2',testingDates2,testingValue2,'r')
    print graph.linedict
    
    #frame.reDraw()
    graph.addPoint('Test Profile 1', datetime.date(2006, 1, 8), 12)
    print graph.linedict
    frame = MainWindow()
    frame.show()
    #frame.canvas.draw()
    #rame.show()
    app.exec_()