import sys
import Tabs
import os
from PySide import QtGui

class GUI(QtGui.QMainWindow):
    
    def __init__(self):
        super(GUI, self).__init__()
        
        self.initUI()
        
    def initUI(self):               
        
        self.setCentralWidget(Tabs.Tabs())

        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        exitAction.setMenuRole(QtGui.QAction.MenuRole.ApplicationSpecificRole);
        
        self.mnuSaveRecipe = QtGui.QAction('Save Recipe..', self)
        self.mnuSaveRecipe.setStatusTip('Save the current recipe')
        self.mnuSaveRecipe.setEnabled(False)
        self.mnuSaveRecipe.setMenuRole(QtGui.QAction.MenuRole.ApplicationSpecificRole);
        
        self.mnuSavePortfolio = QtGui.QAction('Save Portfolio..', self)
        self.mnuSavePortfolio.setStatusTip('Save the current portfolio')
        self.mnuSavePortfolio.setEnabled(True)
        self.mnuSavePortfolio.setMenuRole(QtGui.QAction.MenuRole.ApplicationSpecificRole);
        
        self.mnuSaveRecipeAs = QtGui.QAction('Save Recipe as..', self)
        self.mnuSaveRecipeAs.setStatusTip('Save the current recipe')
        self.mnuSaveRecipeAs.setEnabled(False)
        self.mnuSaveRecipeAs.setMenuRole(QtGui.QAction.MenuRole.ApplicationSpecificRole);
        
        self.mnuSavePortfolioAs = QtGui.QAction('Save Portfolio as..', self)
        self.mnuSavePortfolioAs.setStatusTip('Save the current portfolio')
        self.mnuSavePortfolioAs.setEnabled(True)
        self.mnuSavePortfolioAs.setMenuRole(QtGui.QAction.MenuRole.ApplicationSpecificRole);
        
        self.mnuOpenRecipe = QtGui.QAction('Open Recipe..', self)
        self.mnuOpenRecipe.setStatusTip('Open a recipe')
        self.mnuOpenRecipe.setEnabled(False)
        self.mnuOpenRecipe.setMenuRole(QtGui.QAction.MenuRole.ApplicationSpecificRole);
        
        self.mnuOpenPortfolio = QtGui.QAction('Open Portfolio..', self)
        self.mnuOpenPortfolio.setStatusTip('Open a portfolio')
        self.mnuOpenPortfolio.setEnabled(True)
        self.mnuOpenPortfolio.setMenuRole(QtGui.QAction.MenuRole.ApplicationSpecificRole);

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        
        fileMenu.addAction(self.mnuOpenRecipe)
        fileMenu.addAction(self.mnuOpenPortfolio)
        fileMenu.addAction(self.mnuSaveRecipe)
        fileMenu.addAction(self.mnuSaveRecipeAs)
        fileMenu.addAction(self.mnuSavePortfolio)
        fileMenu.addAction(self.mnuSavePortfolioAs)
        
        fileMenu.addSeparator()
        
        fileMenu.addAction(exitAction)
        

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)

        self.setWindowTitle('TradeUp')
        
        self.setAcceptDrops(True)    
        self.show()
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    sys.path.append(os.path.realpath(__file__)) 
    main()