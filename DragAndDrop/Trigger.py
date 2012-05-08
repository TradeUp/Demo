'''
Created on Apr 21, 2012

@author: Paavan
'''

import PySide
import sys
from PySide import QtCore
from PySide import QtGui
import Function
from backend import *
from FunctionSelector import *
import string

class TriggerWidget(QtGui.QFrame):
    
    request_selection = QtCore.Signal(object);
    request_removal = QtCore.Signal(object);
    
    def __init__(self, parent):
        super(TriggerWidget, self).__init__(parent);
        
        self._layout = QtGui.QVBoxLayout(self);
        
        self._mainTriggerLayout = QtGui.QHBoxLayout();
        
        btnRemove = QtGui.QPushButton("-")
        btnRemove.clicked.connect(self.removeRow);
        btnRemove.setMaximumWidth(20)
        self.setStyleSheet("QFrame { color: #fff; border-radius: 5px; border: 1px solid #777; background: #ccc; }")
        self.leftTarget = FunctionDropTarget()
        self.leftTarget.request_selection.connect(self.selectionRequested)
        self.leftTarget.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.leftTarget.setStyleSheet("QLabel { padding-top:5px; background-color: #eee; border-radius: 5px; color: #555; border: 1px solid #777 }")
        self.leftTarget.setText('this is')
        
        self.rightTarget = FunctionDropTarget()
        self.rightTarget.request_selection.connect(self.selectionRequested)
        self.rightTarget.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.rightTarget.setStyleSheet("QLabel { padding-top:5px; background-color: #eee; border-radius: 5px; color: #555; border: 1px solid #777 }")
        self.rightTarget.setText('that')
        self.combobox = ComparisonComboBox(self);
        
        self._mainTriggerLayout.addWidget(btnRemove,1);
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
        error = False
        
        if(not self.leftTarget.validate()):
            self.setInvalid(self.leftTarget)
            error = True
        
        if not self.rightTarget.validate():
            self.setInvalid(self.rightTarget)
            error = True
        
        if not error and self.leftTarget.function().getUnits() != self.rightTarget.function().getUnits():
            self.setInvalid(self);
            error = True
            
        if error: return None
        
        exprLeft = self.leftTarget.function().getExpression();
        exprRight = self.rightTarget.function().getExpression();
        comparison = self.combobox.currentText()
        
        return RecipeRow(exprLeft, exprRight, comparison);
    
    """
    Set this triggerwidget to match the RecipeRow object passed in
    """
    def setRecipeRow(self, row):
        leftFunction = Function.Function.inflateFunction(row.expr_a)
        rightFunction = Function.Function.inflateFunction(row.expr_b)
        comparator = row.operator
        
        self.leftTarget.setFunction(leftFunction)
        self.leftTarget.setText(FunctionScrollWidget.getDisplayNameForFunction(row.expr_a.funcName))
        
        self.rightTarget.setFunction(rightFunction)
        self.rightTarget.setText(FunctionScrollWidget.getDisplayNameForFunction(row.expr_b.funcName))
        self.combobox.setSelected(comparator)
    
    """
    Mark as invalid: make red
    """
    def setInvalid(self, target):
            target.setStyleSheet("background-color:#FF0000;"); 
        
    """Connected to request_selection signal of FunctionDropTarget class"""
    @QtCore.Slot(object)
    def selectionRequested(self, e):
        #undo marking invalid
#        self.setStyleSheet("border-radius: 5px; border: 1px solid #000");
#        self.leftTarget.setStyleSheet("border-radius: 5px; border: 1px solid #000")
#        self.rightTarget.setStyleSheet("border-radius: 5px; border: 1px solid #000")
        e._target = self;
        self.request_selection.emit(e);
        
    def deselect(self):
        self.leftTarget.deselect();
        self.rightTarget.deselect();
        
    """
    Send the removal request
    """
    @QtCore.Slot(object)
    def removeRow(self):
        self.request_removal.emit(self)
        
        
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
        
    def validate(self):
        if(self.function() == None or not self.function().isValid()):
            return False
        return True
        
    def function(self):
        return self.func;
    
    def setFunction(self, func):
        self.func = func
            
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
            self.func = Function.Function.getFunction(tokens[1])

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
        
        self.setStyleSheet("QFrame { color: #fff; border-radius: 5px; border: 1px solid #777; background: #ccc; }")
        self._layout = QtGui.QHBoxLayout(self);
        
        self._cmbAction = ActionComboBox(self)
        self._cmbUnits = UnitComboBox(self)
        
        self._txtAmount = QtGui.QLineEdit(self)
        self._txtAmount.textChanged.connect(self.resetTextAmount)
        
        self._txtStock = QtGui.QLineEdit(self)
        self._txtStock.textChanged.connect(self.resetTextStock)
        
        lblOf = QtGui.QLabel("of", self)
        lblOf.setMaximumWidth(25)
        
        self._layout.addWidget(self._cmbAction, 1)
        self._layout.addWidget(self._txtAmount, 2)
        self._layout.addWidget(self._cmbUnits, 1)
        self._layout.addWidget(lblOf, 1)
        self._layout.addWidget(self._txtStock, 2)
        
        self.setLayout(self._layout);
        
        self.setMaximumHeight(43);
        
    """
    Convert this trigger into a trigger function
    """
    def convertToTriggerFunc(self):
        
        ticker = self._txtStock.text()
        
        amount = self._txtAmount.text()
        
        unit = self._cmbUnits.getType()
        
        onCall = self._cmbAction.getOnCallFunction()
        
        return Trigger(ticker, amount, unit, onCall)
    
    """
    Convert a trigger function into this trigger object
    """
    def inflateTriggerFunction(self, func):
        self._txtAmount.setText(str(func.amount));
        self._txtStock.setText(func.ticker)
        self._cmbAction.setSelected(func.amount_type)
        if(func.funcName == "buy_stock"):
            self._cmbAction.setSelected("buy")
        elif func.funcName == "sell_stock":
            self._cmbAction.setSelected("sell")
        elif func.funcName == "sell_short":
            self._cmbAction.setSelected("sell short")
        
    """
    Validate this trigger
    """
    def validate(self, controller):
        valid = True
        
        try:
            if int(self._txtAmount.text()) < 0: raise ValueError()
        except ValueError:
            self._txtAmount.setStyleSheet("background-color:#FF0000; border-radius: 5px; border: 1px solid #f33;")
            valid = False
        
        if not controller.validate_ticker(self._txtStock.text()):
            self._txtStock.setStyleSheet("background-color:#FF0000; border-radius: 5px; border: 1px solid #f33;");
            valid = False
            
        return valid
    
    @QtCore.Slot()
    def resetTextStock(self):
        self._txtStock.setStyleSheet("border-radius: 5px; background: #333;");
        
    @QtCore.Slot()
    def resetTextAmount(self):
        self._txtAmount.setStyleSheet("border-radius: 5px; background: #333;");
        
        
class ActionComboBox(QtGui.QComboBox):
    def __init__(self, parent):
        super(ActionComboBox, self).__init__(parent);
        """TODO: implement generic Comparator class, compare two objects of some type """
        
        self.addItem("Buy")
        self.addItem("Sell")
        self.addItem("Sell short")
        
    def getOnCallFunction(self):
        if self.currentText() == "Buy": return "buy_stock"
        else: return "sell_stock"
        
    """
    Set the specified action as selected
    """
    def setSelected(self, action):
        if string.lower(action) == "buy":
            self.setCurrentIndex(0)
        elif string.lower(action) == "sell":
            self.setCurrentIndex(1)
        elif string.lower(action) == "sell short":
            self.setCurrentIndex(2)
        
class UnitComboBox(QtGui.QComboBox):
    def __init__(self, parent):
        super(UnitComboBox, self).__init__(parent);
        """TODO: implement generic Comparator class, compare two objects of some type """
        
        self.addItem("Shares")
        self.addItem("Dollars")
        
    def getType(self):
        if self.currentText() == "Shares": return 'SHARES'
        else: return 'DOLLARS'
        
    def setSelected(self, unit):
        if string.lower(unit) == "shares":
            self.setCurrentIndex(0)
        elif string.lower(unit) == "dollars":
            self.setCurrentIndex(1)
        
class ComparisonComboBox(QtGui.QComboBox):
    def __init__(self, parent):
        super(ComparisonComboBox, self).__init__(parent);
        """TODO: implement generic Comparator class, compare two objects of some type """
        
        self.addItem("<")
        self.addItem("<=")
        self.addItem("=")
        self.addItem(">")
        self.addItem(">=")
        
    """
    Set the indicated operator as selected
    """
    def setSelected(self, operator):
        if operator == "<":
            self.setCurrentIndex(0)
        elif operator == "<=":
            self.setCurrentIndex(1)
        elif operator == "=" or operator == "==":
            self.setCurrentIndex(2)
        elif operator == ">":
            self.setCurrentIndex(3)
        elif operator == ">=":
            self.setCurrentIndex(4)