import PySide
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from recipes import  *
from Inspector import *
from ActionPanel import *

class Button(QLabel):
    def __init__(self, title, parent, data):
        super(Button, self).__init__(title, parent);
        self.data = data;
        
    def mouseMoveEvent(self, e):
        #don't drag if left cick
        if e.buttons() == Qt.RightButton:
            return
        
        mimeData = QMimeData()
        
        drag = QDrag(self);
        
        mimeData.setText(self.data);
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos()-self.rect().topLeft());
        
        #draw the right pixmap
        pixmap = QPixmap()
        pixmap = pixmap.grabWidget(self);
        
        drag.setPixmap(pixmap);
        
        drag.start(Qt.MoveAction);
        
class Label(QLabel):
    def __init__(self, title, parent):
        super(Label, self).__init__(title, parent);
        self.setMinimumWidth(50);
        self.setAcceptDrops(True)
        
    
    def dragEnterEvent(self, e):
        if(e.mimeData().hasFormat("text/plain")):
            e.accept();
    
    def dragLeaveEvent(self, e):
        self.setStyleSheet("");
        self.repaint()
            
    def dragMoveEvent(self, e):
        e.accept()
        if(e.mimeData().text() == "Accept"):
            self.setStyleSheet("QLabel { background-color:#00FF00 }")
            self.repaint();
        else:
            self.setStyleSheet("QLabel { background-color:#FF0000 }")
            self.repaint();
        
    def dropEvent(self, e):
        if(e.mimeData().text() == "Accept"):
            self.setText("Accepted!");
            e.accept();
        else: 
            e.ignore();
            self.setText("Rejected!");
        self.setStyleSheet("");
        self.repaint();

class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__();
        self.initUI();
        
    def initUI(self):
        self.setAcceptDrops(True)
        
        rootHLayout = QtGui.QHBoxLayout();
        vLayout1 = QtGui.QVBoxLayout();
        
        self.inspector = Inspector()
        vLayout1.addWidget(self.inspector);
        
        rootHLayout.addLayout(vLayout1);
        
        self.list = RecipeList();
        self.list.setBackgroundRole(QtGui.QPalette.ColorRole.Light);
        self.list.setMinimumWidth(250)
        
        self.list.addEmptyTrigger();
        self.list.addEmptyTrigger();
        self.list.addEmptyTrigger();
        
        self.list.setMaximumHeight(100);
        
        #connect the list's function_selected signal to the inspector's setEditor slot
        #This will make the inspector update its editor every time a function is selected
        self.list.function_selected.connect(self.inspector.setEditor)
        
        rootHLayout.addWidget(self.list);
        
        self.pnlBuyActions = ActionPanel(self);
        self.pnlBuyActions.setBackgroundRole(QtGui.QPalette.ColorRole.Light);
        self.pnlBuyActions.setMinimumWidth(300)
        
        self.pnlBuyActions.addEmptyTrigger();
        self.pnlBuyActions.setMaximumHeight(100);
        rootHLayout.addWidget(self.pnlBuyActions)
        
        self.setLayout(rootHLayout);
        
        self.setGeometry(300,300,600,300);
        
        self.setWindowTitle('Click or Move');
        self.show()
    
def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main();