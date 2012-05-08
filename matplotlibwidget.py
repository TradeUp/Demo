'''
Created on Mar 23, 2012

@author: WillIV
'''
import matplotlib
import numpy as np


matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'


from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas



class MatplotlibWidget(FigureCanvas):

    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(Figure())

        self.setParent(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)


    def Plot(self):


        data1 = np.loadtxt('FStream.dat')
        data2 = np.loadtxt('FShield.dat')

        self.axes.plot(data1[0],data1[1],data2[0],data2[1])
        self.canvas.draw()