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

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
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