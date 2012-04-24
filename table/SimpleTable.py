import sys
from PySide.QtCore import *
from PySide.QtGui import *

#window width and height constants (change, if you please)
WINDOW_W = 600
WINDOW_H = 250
ADD_BUTTON_H = 25
ADD_BUTTON_W = 100

    
#Button to add recipes, pushing on it displays a file selection dialog
class AddButton(QPushButton):
    
    def __init__(self, table):
        super(AddButton, self).__init__()
        self.setText("Add Recipe")
        self.setFixedSize(ADD_BUTTON_W, ADD_BUTTON_H)
        self.clicked.connect(self.chooseFile)
        self.table = table

        
    def chooseFile(self):
        fileName = QFileDialog.getOpenFileName(self, dir="/home/dylan/mock_algo/", filter="*.algo")
        print fileName
        #add some method to send file name to backend here!!
        """ADD FUNCTION HERE...LET IT RETURN TRUE IF VALID FILE"""
        valid = True
        if valid:
            """get actual name later-->probably should be a JSON field"""
            name = "Name %s" % self.table.rowCount()
            self.table.addRecipe(name)
            
    

class RemoveButton(QPushButton):
    
    def __init__(self, table, row):
        super(RemoveButton, self).__init__()
        self.setIcon(QIcon("/home/dylan/Desktop/remove_button.png")) 
        self.table = table
        self.row = row
        self.clicked.connect(self.remove)
        self.pressed.connect(self.remove)
        
    def updateRow(self, row):
        self.row = row
    
    def remove(self):
        print "removing recipe " + str(self.row)
        self.table.removeRow(self.row)
        self.table.notifyRows(self.row)
        


class Table(QTableWidget):
    
    def __init__(self):
        super(Table, self).__init__(1, 5) #init with one row, 5 columns
        
        #set horizontal headers
        headers = ["Recipe", "Value", "P/L", "% Return", "Remove?"]
        self.setHorizontalHeaderLabels(headers)
        
        #add total row
        for col in xrange(0,5):                
            grayItem = QTableWidgetItem()
            grayItem.setBackground(QBrush(QColor("lightgray")))
            grayItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            if col is 0:
                grayItem.setFont(QFont("Arial", 15, QFont.Bold))
                grayItem.setText("Total:")
            elif col is 3:
                grayItem.setText("0.000%")
            elif col < 4:
                grayItem.setText("$0")
            self.setItem(0, col, grayItem)
        
        #hide vertical header
        self.verticalHeader().hide()
        
        
    def addRecipe(self, name):
        #TODO: add color!!!
        rows = self.rowCount()
        #expand the table by one row
        self.setRowCount(rows + 1)
        
        #add name cell with checkbox
        nameItem = QTableWidgetItem(name)
        nameItem.setCheckState(Qt.Checked)
        nameItem.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable)
        self.setItem(rows, 0, nameItem)
        
        #set default values for other cells:
        defaultValueItem = QTableWidgetItem("$0")
        self.setItem(rows, 1, defaultValueItem)
        defaultPLItem = QTableWidgetItem("$0")
        self.setItem(rows, 2, defaultPLItem)
        defaultPercentItem = QTableWidgetItem("%0")
        self.setItem(rows, 3, defaultPercentItem)
            
        
        #add in remove button
        rmButton = RemoveButton(self, rows)
        self.setCellWidget(rows, 4, rmButton)
        
    def notifyRows(self, rowRemoved):
        for row in xrange(rowRemoved, self.rowCount()):
            button = self.cellWidget(row, 4)
            button.updateRow(button.row - 1)
    
    def setTotalRowValue(self, value):
        """sets the total row's value cell"""
        pass
        
    def setTotalRowPL(self, value):
        """sets the total row's P/L cell"""
        pass
    
    def setTotalRowPercent(self, name, value):
        """sets the total row's percent cell"""
        pass
    
    def setRecipeValue(self, name, value):
        """sets the recipe's value cell 
        to the given value"""
        pass
    
    def setRecipePL(self, name, value):
        """sets the recipe's P/L cell 
        to the given value"""
        pass
    
    def setRecipePercent(self, name, value):
        """sets the recipe's percent cell
        to the given value (Note: value should
        be expressed in basis point form.  I.e.
        passing in .37 will render 0.37%)"""
        pass


class Window(QWidget):
    
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, WINDOW_W, WINDOW_H)
        self.setWindowTitle("Recipes")
        table = Table()
        addButton = AddButton(table)
        
        
        layout = QVBoxLayout()
        layout.addWidget(table)
        layout.addWidget(addButton)        
        
        self.setLayout(layout)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())

