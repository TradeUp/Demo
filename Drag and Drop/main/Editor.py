'''
Created on Apr 21, 2012

@author: Paavan
'''
import PySide
import sys
from PySide import QtCore
from PySide import QtGui

"""Basic Editor widget, allowing the editing of a """
class BasicEditor(QtGui.QFrame):
    
    """
    func- SimpleFunction object to modify
    """
    def __init__(self, parent, func):
        super(BasicEditor, self).__init__()
        
        