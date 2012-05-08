#import PySide
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from recipes import  *
from Inspector import *
from ActionPanel import *
from FunctionSelector import *
from backend import *
import os

class RecipeWindow(QWidget):
    def __init__(self, controller, recipeName=None):
        super(RecipeWindow, self).__init__();
        self.setAcceptDrops(True)
        self.recipeName = recipeName
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
        # set up the buttons
        btnAddRow = QtGui.QPushButton("Add Row");
        
        # label that stores the name of the recipe
        self.lblName = QtGui.QLabel("Untitled", self)
        self.lblName.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        
        self.list = RecipeList();
        self.list.setBackgroundRole(QtGui.QPalette.ColorRole.Light)
        self.list.setMinimumWidth(300)
        
        self.list.addEmptyTrigger();
        
        #connect the list's function_selected signal to the inspector's setEditor slot
        #This will make the inspector update its editor every time a function is selected
        self.list.function_selected.connect(self.inspector.setEditor)
        
        #Connect the btnAddRow clicked signal to add a new row in the recipe list
        btnAddRow.clicked.connect(self.list.addEmptyTrigger)
        
        vLayout2 = QtGui.QGridLayout();
        vLayout2.addWidget(self.lblName, 0,0,1,1)
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
        
    """
    Bring up a file dialog so the user can save the recipe
    """
    def saveRecipeAs(self):
        #bring up a file dialog so they can save it
        self.recipeName = QFileDialog.getSaveFileName(self, dir="/home/dylan/mock_algo/", filter="*.algo")[0]
        if self.recipeName == '':
            self.recipeName = None
            return
        
        self.lblName.setText(os.path.basename(self.recipeName))
        
        self.saveRecipeWithName(self.recipeName)
        
    def saveRecipe(self):
        self.saveRecipeWithName(self.recipeName)
        
    def saveRecipeWithName(self,name):
        if(self.recipeName == None):
            self.saveRecipeAs()
            return
        
        if(self.list.numTriggers() == 0):
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Critical, "Error", "");
            msgBox.setText("A recipe must have at least one trigger to be able to save.")
            msgBox.exec_()
            return
        
        recipe = self.list.createRecipe()
        
        if not recipe:
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Critical, "Error", "")
            msgBox.setText("There was an error saving the recipe! Fix the red triggers and try again.")
            msgBox.exec_()
            return
        
        if not self.pnlBuyActions.validate(self.controller):
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Critical, "Error", "")
            msgBox.setText("There was an error saving the recipe! Fix the buy action and try again.")
            msgBox.exec_()
            return
        
        triggerFunc = self.pnlBuyActions.getTrigger().convertToTriggerFunc()
        
        recipe.trigger = triggerFunc
        recipe.name = name.rsplit('/')[-1]
        recipe.to_file(self.recipeName);
       
        #save successful
        msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Information, "Success!", "")
        msgBox.setText("Recipe successfully saved!")
        msgBox.exec_()
        
    def openRecipe(self):
        #bring up a file dialog so they can open it
        path = QFileDialog.getOpenFileName(self, dir="/home/dylan/mock_algo/", filter="*.algo")[0]
        if path == '':
            return
        
        parser = Parser(None)
        
        recipe = None
        try:
            recipe = parser.parse_recipe(path)
        except:
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Critical, "Error", "");
            msgBox.setText("Unable to open file.")
            msgBox.exec_()
            return
        
        self.list.loadRecipe(recipe)
            
        self.pnlBuyActions.loadRecipe(recipe);
    
        self.recipeName = path
        self.lblName.setText(os.path.basename(self.recipeName))
    
def main():
    app = QApplication(sys.argv)
    ex = RecipeWindow()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()

