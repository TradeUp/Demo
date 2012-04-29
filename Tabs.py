#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
#############################################################################

import sys
import GraphTable
import GraphUI
import graph
import datetime
from GraphTable import Testing
from PySide import QtGui, QtCore
from PySide.QtCore import *
from backend import Parser,Recipe 
from PySide.QtGui import *
from SimpleTable import AddButton,Table
import DragAndDrop




class Tabs(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        testingDates1 = [datetime.date(2006, 1, 3), datetime.date(2006, 1, 4),datetime.date(2006, 1, 5),datetime.date(2006, 1, 6),datetime.date(2006, 1, 7)]
        testingValue1 = [1,2,3,10,7]
        testingDates2 = [datetime.date(2006, 1, 5), datetime.date(2006, 1, 6),datetime.date(2006, 1, 7),datetime.date(2006, 1, 8),datetime.date(2006, 1, 9)]
        testingValue2 = [10,20,30,15,7]
    
        graph.makeLine('Test Profile 1',testingDates1,testingValue1,'b')
        graph.makeLine('Test Profile 2',testingDates2,testingValue2,'r')
        print graph.linedict
       
        frame = GraphUI.MainWindow()
        self.controller = Controller(None,None)
        ex = GraphTable.GraphTable(frame,controller)
        # set the graph too
        self.controller.table = ex.table 
        frame.controller = self.controller
        # now the frame is the graph (i.e. has the method makenew)
        self.controller.graph = frame 

        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(ex,"Graph")
        tabWidget.addTab(DragAndDrop.RecipeWindow(), "Kitchen") 
      
        okButton = QtGui.QPushButton(self.tr("OK"))
        cancelButton = QtGui.QPushButton(self.tr("Cancel"))

        self.connect(okButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("accept()"))
        self.connect(cancelButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("reject()"))

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle("TradeUp")

    def run_test(self):
        # run the controller evaluating in a loop
        for x in xrange(100):
            self.controller.eval(x) # every other one should be true (xing fingers)

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
