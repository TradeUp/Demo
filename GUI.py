
import sys
import Tabs
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

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)

        self.setWindowTitle('TradeUp')    
        self.show()
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()