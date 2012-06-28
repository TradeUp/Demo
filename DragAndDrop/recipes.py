'''
Created on Mar 15, 2012

@author: Paavan
'''
import sys
from PySide import QtCore, QtGui
import Function
from Trigger import *
from backend import *

class RecipeList(QtGui.QScrollArea):
    
    #Create a signal to communicate the function selected
    function_selected = QtCore.Signal(object)
    
    def __init__(self):
        super(RecipeList, self).__init__()
        
        self._triggers = []
        self._selectedTrigger = None
        
        #dummy root widget to hold everything. QScrollArea needs this to be able to scroll
        root = QtGui.QWidget();
        
        #add a vertical box layout to order the recipes
        self._layout = QtGui.QVBoxLayout()
        self._layout.setContentsMargins(0,0,0,0);
        root.setLayout(self._layout);
        
        self.setWidget(root);
        self.setWidgetResizable(True);
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff);
        
    def addEmptyTrigger(self):
        self.addTrigger(TriggerWidget(self))
        
    def addTrigger(self, trigger):
        trigger.request_selection.connect(self.selectionRequested);
        trigger.request_removal.connect(self.removeRequested);
        
        trigger.setMaximumWidth(self.size().width());
        trigger.setMaximumHeight(50);
        self._triggers.append(trigger);
        self._layout.addWidget(trigger);
        
        root = QtGui.QWidget();
        root.setLayout(self._layout);
        self.setWidget(root);
        root.show();
        
    def numTriggers(self):
        return len(self._triggers)
    
    def loadRecipe(self, recipe):
        #first, clear the list of all triggers
        self.clearList();
        
        print "LOADING RECIPES"
        #iterate through all the rows, adding each one one by one
        for row in recipe.rows:
            print "LOADING TRIGGER"
             
            trigger = TriggerWidget(self)
            trigger.setRecipeRow(row)
            
            self.addTrigger(trigger)
        print "FINISHED"
        
    """
    Remove all the trigger rows from the list
    """
    def clearList(self):
        for row in self._triggers:
            if self._selectedTrigger == row: self._selectedTrigger = None;
            self._layout.removeWidget(row)
            row.deleteLater();
            
        self._triggers = []
    
    """
    Create a Recipe object with rows
    """
    def createRecipe(self):
        recipe = Recipe();
        
        #add all the triggers
        print "CREATING RECIPE FROM: ", self._triggers
        for trigger in self._triggers:
            row = trigger.getRecipeRow();
            
            #do not save if there is an error!
            if(row != None):
                recipe.add_row(trigger.getRecipeRow())
            else:
                return None
            
        return recipe
                
    @QtCore.Slot(object)
    def selectionRequested(self, e):
        print "selected a function!"
        #accept the selection
        if(self._selectedTrigger != None):
            self._selectedTrigger.deselect();
        self._selectedTrigger = e.target();
        e.accept();
        
        #emit the function selected event to all listeners
        self.function_selected.emit(e.function());
        
    """
    Slot that allows the removal of a recipe row
    """
    @QtCore.Slot(object)
    def removeRequested(self, row):
        if self._selectedTrigger == row: self._selectedTrigger = None;
        
        self._triggers.remove(row)
        
        print self._triggers
        
        self._layout.removeWidget(row)
        row.deleteLater();