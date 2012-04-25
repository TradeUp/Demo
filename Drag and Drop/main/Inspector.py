'''
Created on Apr 14, 2012

@author: Paavan
'''
import PySide
import sys
from PySide import QtCore
from PySide import QtGui

class Inspector(QtGui.QFrame):
    def __init__(self):
        super(Inspector, self).__init__();
        
        #default message.
        self.lblEmpty = QtGui.QLabel("No function selected.");
        
        layout = QtGui.QVBoxLayout();
        layout.addWidget(self.lblEmpty);
        
        self.setLayout(layout);
        
    '''Set the editor for this inspector, given a function object'''
    @QtCore.Slot(object)
    def setEditor(self, func):
        print "SETTING EDITOR FOR FUNCTION"
        pass