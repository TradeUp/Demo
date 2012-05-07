'''
Created on Apr 21, 2012

@author: Paavan
'''
import PySide
import sys
from PySide import QtCore
from PySide import QtGui
from Trigger import ActionTrigger

class ActionPanel(QtGui.QScrollArea):
    def __init__(self, parent):
        super(ActionPanel, self).__init__(parent);
        
        #store all triggers
        self._triggers = [];
        
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
        trigger = ActionTrigger(self);
        trigger.setMaximumWidth(self.size().width());
        self._triggers.append(trigger);
        self._layout.addWidget(trigger);
        
        root = QtGui.QWidget();
        root.setLayout(self._layout);
        self.setWidget(root);
        root.show();
        
    def getTrigger(self):
        #trigger = self._triggers[0]
        return self._triggers[0]
    
    """
    Validate the triggers
    """
    def validate(self, controller):
        valid = True
        for trigger in self._triggers:
            if not trigger.validate(controller): valid = False
        
        return valid
        