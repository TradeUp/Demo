import sys
import Tabs
import os
from PySide import QtGui
import yfinance

class GUI(QtGui.QMainWindow):
    
    def __init__(self):
        super(GUI, self).__init__()
        print "starting to run..1"
        self.initUI()
        
    def initUI(self): 
        print "starting to run..2"
        """try:
            yfinance.get_price('aapl')
        except:
            error = QtGui.QErrorMessage()
            error.showMessage('Error Establishing Internet Connection')
            error.exec_()
            self.destroy()
            return """
        print "starting to run..3"
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

        self.setWindowTitle('TradeUp')
        self.setMinimumSize(900,600)
        self.showFullScreen()
        self.showMaximized()
        self.setAcceptDrops(True)  
        self.show()


def main():

    
    QtGui.QApplication.setStyle('motif')
    app = QtGui.QApplication(sys.argv)

    gui = GUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    sys.path.append(os.path.realpath(__file__)) 
    main()