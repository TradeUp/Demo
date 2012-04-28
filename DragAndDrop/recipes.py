'''
Created on Mar 15, 2012

@author: Paavan
'''
import PySide
import sys
from PySide import QtCore
from PySide import QtGui
import Function
from Trigger import *
from backend import *

class RecipeList(QtGui.QScrollArea):
    
    #Create a signal to communicate the function selected
    function_selected = QtCore.Signal(object);
    
    def __init__(self):
        super(RecipeList, self).__init__();
        
        self._triggers = [];
        self._selectedTrigger = None;
        
        #dummy root widget to hold everything. QScrollArea needs this to be able to scroll
        root = QtGui.QWidget();
        
        #add a vertical box layout to order the recipes
        self._layout = QtGui.QVBoxLayout();
        self._layout.setContentsMargins(0,0,0,0);
        root.setLayout(self._layout);
        
        self.setWidget(root);
        self.setWidgetResizable(True);
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff);
        
    def addEmptyTrigger(self):
        trigger = TriggerWidget(self);
        trigger.request_selection.connect(self.selectionRequested);
        trigger.setMaximumWidth(self.size().width());
        self._triggers.append(trigger);
        self._layout.addWidget(trigger);
        
        root = QtGui.QWidget();
        root.setLayout(self._layout);
        self.setWidget(root);
        root.show();
    
    """
    Create a Recipe object with rows
    """
    def createRecipe(self):
        recipe = Recipe();
        
        #add all the triggers
        for trigger in self._triggers:
            row = trigger.getRecipeRow();
            
            if(row != None):
                recipe.add_row(trigger.getRecipeRow())
            
        return recipe
                
    @QtCore.Slot(object)
    def selectionRequested(self, e):
        #accept the selection
        if(self._selectedTrigger != None):
            self._selectedTrigger.deselect();
        self._selectedTrigger = e.target();
        e.accept();
        
        #emit the function selected event to all listeners
        self.function_selected.emit(e.function());