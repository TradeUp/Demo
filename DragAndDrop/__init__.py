import PySide
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from recipes import  *
from Inspector import *
from ActionPanel import *
from FunctionSelector import *

class RecipeWindow(QWidget):
    def __init__(self, portfolio=None):
        super(RecipeWindow, self).__init__();
        self.initUI();
        
        self.portfolio = portfolio;
        if(self.portfolio == None):
            self.portfolio = Portfolio();
        
    def initUI(self):
        self.setAcceptDrops(True)
        
        rootHLayout = QtGui.QHBoxLayout();
        vLayout1 = QtGui.QVBoxLayout();
        
        self.functionList = FunctionScrollWidget()
        vLayout1.addWidget(self.functionList)
        
        self.inspector = Inspector()
        self.inspector.setMinimumHeight(150);
        vLayout1.addWidget(self.inspector);
        
        rootHLayout.addLayout(vLayout1);
        
        btnSave = QtGui.QPushButton("Save");
        
        btnAddRow = QtGui.QPushButton("Add Row");
        
        self.list = RecipeList();
        self.list.setBackgroundRole(QtGui.QPalette.ColorRole.Light);
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
        
        self.setLayout(rootHLayout);
        
        self.setGeometry(300,300,600,300);
        
        self.setWindowTitle('Click or Move');
        self.show()
        
    def saveRecipe(self):
        recipe = self.list.createRecipe()
        
        recipe.trigger = Trigger("test_oncall");
            
        self.portfolio.add_recipe(recipe);
        
        self.portfolio.to_file("test.algo");
        
        return self.portfolio
    
def main():
    app = QApplication(sys.argv)
    ex = RecipeWindow()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main();