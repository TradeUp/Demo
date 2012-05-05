#import PySide
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from recipes import  *
from Inspector import *
from ActionPanel import *
from FunctionSelector import *
from backend import *

class RecipeWindow(QWidget):
    def __init__(self, controller, portfolio=None):
        super(RecipeWindow, self).__init__();
        self.setAcceptDrops(True)
        self.portfolio = portfolio or Portfolio()
        self.controller = controller
        self.initUI()

        
    def initUI(self):
        self.setAcceptDrops(True)
        # establish layout
        rootHLayout = QtGui.QHBoxLayout()
        vLayout1 = QtGui.QVBoxLayout()
        # functions
        self.functionList = FunctionScrollWidget()
        vLayout1.addWidget(self.functionList)
        # create the inspector
        self.inspector = Inspector(self.controller)
        self.inspector.setMinimumHeight(150)
        vLayout1.addWidget(self.inspector)
        # add the vLayout to the root
        rootHLayout.addLayout(vLayout1);
        # set up the bottons
        btnSave = QtGui.QPushButton("Save");
        btnAddRow = QtGui.QPushButton("Add Row");
        
        self.list = RecipeList();
        self.list.setBackgroundRole(QtGui.QPalette.ColorRole.Light)
        self.list.setMinimumWidth(250)
        
        self.list.addEmptyTrigger();
        
        #connect the list's function_selected signal to the inspector's setEditor slot
        #This will make the inspector update its editor every time a function is selected
        self.list.function_selected.connect(self.inspector.setEditor)
        
        #Connect the btnAddRow clicked signal to add a new row in the recipe list
        btnAddRow.clicked.connect(self.list.addEmptyTrigger)
        #allow saving
        btnSave.clicked.connect(self.saveRecipe)
        
        vLayout2 = QtGui.QGridLayout();
        vLayout2.addWidget(btnSave,   0, 0, 1, 1)
        vLayout2.addWidget(btnAddRow, 1, 0, 1, 1)
        vLayout2.addWidget(self.list, 2, 0, 10, 1)
        
        
        rootHLayout.addLayout(vLayout2);
        
        self.pnlBuyActions = ActionPanel(self);
        self.pnlBuyActions.setBackgroundRole(QtGui.QPalette.ColorRole.Light);
        self.pnlBuyActions.setMinimumWidth(300)
        
        self.pnlBuyActions.addEmptyTrigger();
        #self.pnlBuyActions.setMaximumHeight(100);
        rootHLayout.addWidget(self.pnlBuyActions)
        
        # window code
        self.setLayout(rootHLayout); 
        self.setGeometry(300,300,600,300);    
        self.setWindowTitle('Click or Move');
        self.show()
        
    def saveRecipe(self):
        recipe = self.list.createRecipe()
        
        triggerFunc = self.pnlBuyActions.getTrigger().convertToTriggerFunc()
        
        recipe.trigger = triggerFunc
            
        recipe.to_file("test.algo");
        
        #return self.portfolio
    
def main():
    app = QApplication(sys.argv)
    ex = RecipeWindow()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()

