import sys
import platform
import datetime
import numpy as np
import PySide
from PySide.QtGui import * 
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

    linedict = {'Default': ([datetime.date(2001, 3, 5), datetime.date(2001, 3, 6)], [1,5])}
    unusedColors = ['b', 'g', 'r','c','m','y','k']
    usedColors = []

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        self.controller = None # this is set in tabs
        self.main_frame = QWidget()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent( self.main_frame )     
        self.reDraw()
        
    def OOps(self, data):
        self.linedict.clear()
        for n in data:
            # n = name/key
            # need to take (amnt,price) -> amnt*price 
            self.linedict[n] = data[n]
        self.reDraw()
        
    def reDraw(self):
        self.figure.clear()
        self.axes = self.figure.add_subplot(111)
        self.axes.grid(color='0.75', linestyle='-', linewidth=0.5)      
        color = ''
        superMax = 0
        superMin = float('inf')
        for line in self.linedict.items():
            if(len(self.unusedColors) >= 1):
                color = self.unusedColors[0]
                self.usedColors.append(self.unusedColors[0])
                del self.unusedColors[0]
            else:
                color = self.usedColors[0]
                unusedColors = self.usedColors[1:]
                usedColors = self.usedColors[:1]

            print line[1]
            yaxis = line[1][1]
            xaxis = line[1][0]
            j = max(yaxis)- min(yaxis)
            x = j*.1
            newMax = max(yaxis) + x
            newMin = min(yaxis) - x
            if(newMax > superMax):
                superMax = newMax
            if(newMin < superMin):
                superMin = newMin  
            self.axes.plot(xaxis,yaxis, color=color, label=line[0])
        self.axes.set_ylim([superMin,superMax])  

        props = font_manager.FontProperties(size=10)
        self.axes.legend(loc='center left', shadow=True, fancybox=True, prop=props)
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)
        self.canvas.draw()
        
    def testing(self):
        print 'hi'

    def update(self,data,table,table_data):
        print "Update called on", data
        graph.makenew(self, data)
        table.update(table_data)
    
    def up(self):
        frame.redraw();

if __name__ == '__main__':
    app = QApplication(sys.argv)
#    testingDates1 = [datetime.date(2006, 1, 3), datetime.date(2006, 1, 4),datetime.date(2006, 1, 5),datetime.date(2006, 1, 6),datetime.date(2006, 1, 7)]
#    testingValue1 = [1,2,3,10,7]
#    testingDates2 = [datetime.date(2006, 1, 5), datetime.date(2006, 1, 6),datetime.date(2006, 1, 7),datetime.date(2006, 1, 8),datetime.date(2006, 1, 9)]
#    testingValue2 = [10,20,30,15,7]
#    
#    graph.makeLine('Test Profile 1',testingDates1,testingValue1,'b')
#    graph.makeLine('Test Profile 2',testingDates2,testingValue2,'r')
#    print graph.linedict
#    
#    #frame.reDraw()
#    graph.addPoint('Test Profile 1', datetime.date(2006, 1, 8), 12)
#    print graph.linedict
    frame = MainWindow()
    frame.show()
    #frame.canvas.draw()
    #rame.show()
    app.exec_()