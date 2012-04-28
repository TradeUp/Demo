'''
Created on Apr 21, 2012

@author: Paavan
'''

import PySide
import sys
from PySide import QtCore
from PySide import QtGui
from Function import Function
from backend import *

class TriggerWidget(QtGui.QFrame):
    
    request_selection = QtCore.Signal(object);
    
    def __init__(self, parent):
        super(TriggerWidget, self).__init__(parent);
        
        self._layout = QtGui.QVBoxLayout(self);
        
        self._mainTriggerLayout = QtGui.QHBoxLayout();
        
        self.leftTarget = FunctionDropTarget()
        self.leftTarget.request_selection.connect(self.selectionRequested);
        self.leftTarget.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter);
        self.leftTarget.setStyleSheet("QLabel { padding-top:5px; }")
        
        self.rightTarget = FunctionDropTarget()
        self.rightTarget.request_selection.connect(self.selectionRequested);
        self.rightTarget.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter);
        self.rightTarget.setStyleSheet("QLabel { padding-top:5px; }")
        
        self.combobox = ComparisonComboBox(self);
        
        self._mainTriggerLayout.addWidget(self.leftTarget,5);
        self._mainTriggerLayout.addWidget(self.combobox,1);
        self._mainTriggerLayout.addWidget(self.rightTarget,5);
        
        
        self._layout.addLayout(self._mainTriggerLayout);
        
        self.setLayout(self._layout);
        
        self.setAcceptDrops(True);
    
    """
    Convert this trigger into a recipe row object.
    Returns None if invalid row.
    """
    def getRecipeRow(self):
        #If one of the functions are None or the units don't match, return None
        if(self.leftTarget.function() == None or self.rightTarget.function() == None
           or self.leftTarget.function().getUnits() != self.rightTarget.function().getUnits()):
            self.setInvalid();
            return None;
        
        exprLeft = self.leftTarget.function().getExpression();
        exprRight = self.rightTarget.function().getExpression();
        comparison = self.combobox.currentText()
        
        return RecipeRow(exprLeft, exprRight, comparison);
    
    """
    Mark as invalid: make red
    """
    def setInvalid(self):
            self.setStyleSheet("background-color:#FF0000;"); 
        
    """Connected to request_selection signal of FunctionDropTarget class"""
    @QtCore.Slot(object)
    def selectionRequested(self, e):
        #undo marking invalid
        self.setStyleSheet("");
        e._target = self;
        self.request_selection.emit(e);
        
    def deselect(self):
        self.leftTarget.deselect();
        self.rightTarget.deselect();
        
        
class FunctionDropTarget(QtGui.QLabel):
    
    #Create a signal to tell the parent that this function target is requesting selection
    request_selection = QtCore.Signal(object);
    
    def __init__(self, text="None"):
        super(FunctionDropTarget, self).__init__(text);
        
        self.setAcceptDrops(True);
        
        #at first, this target does not represent a function
        self.func = None
        
        palette = self.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(0,0,255));
        self.setPalette(palette);
        self.setAutoFillBackground(True);
        
    def function(self):
        return self.func;
            
    def dragEnterEvent(self, e):
        print "DRAG ENTER"
        e.accept();
        
    def dragLeaveEvent(self, e):
        print "DRAG LEAVE"
        e.accept();
        
    def dropEvent(self, e):
        print "DROPPED"
        #parse the data into a function object
        if e.mimeData().hasFormat('text/plain'):
            tokens = e.mimeData().text().split('/');

            self.setText(tokens[0])
            self.func = Function.getFunction(tokens[1])

            #send the request selection signal
            self.request_selection.emit(FunctionSelectionEvent(self, self.func, self.onSelected));

            e.setDropAction(QtCore.Qt.CopyAction);
            e.accept()
        else:
            e.ignore() 
        
        

        
    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.request_selection.emit(FunctionSelectionEvent(self, self.func, self.onSelected));
            
    def onSelected(self):
        self.setBackgroundRole(QtGui.QPalette.ColorRole.Highlight);
    
    def deselect(self):
        self.setBackgroundRole(QtGui.QPalette.ColorRole.Base);
        
class FunctionSelectionEvent():
    """
    Take the object requesting selection, and the function to call should this event be accepted
    """
    def __init__(self, target, function, onAccept):
        self._target = target;
        self._func = function;
        self._onAccept = onAccept;
        
    def accept(self):
        self._onAccept();
        
    def ignore(self):
        pass
        
    def target(self):
        return self._target;
    
    def function(self):
        return self._func;

class ActionTrigger(QtGui.QFrame):
    def __init__(self, parent):
        super(ActionTrigger, self).__init__(parent)
        
        self._layout = QtGui.QHBoxLayout(self);
        
        self._cmbAction = ActionComboBox(self)
        self._cmbUnits = UnitComboBox(self)
        
        self._txtAmount = QtGui.QTextEdit(self)
        self._txtStock = StockChooser(self)
        
        self._layout.addWidget(self._cmbAction, 1)
        self._layout.addWidget(self._txtAmount, 2)
        self._layout.addWidget(self._cmbUnits, 1)
        self._layout.addWidget(self._txtStock, 2)
        
        self.setLayout(self._layout);
        
        self.setMaximumHeight(43);
        
class StockChooser(QtGui.QTextEdit):
    def __init__(self, parent):
        super(StockChooser, self).__init__(parent)
        
class ActionComboBox(QtGui.QComboBox):
    def __init__(self, parent):
        super(ActionComboBox, self).__init__(parent);
        """TODO: implement generic Comparator class, compare two objects of some type """
        
        self.addItem("Buy")
        self.addItem("Sell")
        self.addItem("Sell short")
        
class UnitComboBox(QtGui.QComboBox):
    def __init__(self, parent):
        super(UnitComboBox, self).__init__(parent);
        """TODO: implement generic Comparator class, compare two objects of some type """
        
        self.addItem("Shares")
        self.addItem("Dollars")
        
class ComparisonComboBox(QtGui.QComboBox):
    def __init__(self, parent):
        super(ComparisonComboBox, self).__init__(parent);
        """TODO: implement generic Comparator class, compare two objects of some type """
        
        self.addItem("<")
        self.addItem("<=")
        self.addItem("=")
        self.addItem(">")
        self.addItem(">=")