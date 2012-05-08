import sys
import Tabs
import os
from PySide import QtGui

class GUI(QtGui.QMainWindow):
    
    def __init__(self):
        super(GUI, self).__init__()
        
        self.initUI()
        
    def initUI(self):               
        
        tabs = Tabs.Tabs()
        self.setCentralWidget(tabs)

        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        exitAction.setMenuRole(QtGui.QAction.MenuRole.ApplicationSpecificRole);

        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('&File')
        
        tabs.addMenuItems(fileMenu)
        
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