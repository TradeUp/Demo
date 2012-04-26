import sys
from PySide.QtCore import *
from backend import Parser,Recipe 
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
        self.controller = table.controller

        
    def chooseFile(self):
        fileName = QFileDialog.getOpenFileName(self, dir="/home/dylan/mock_algo/", filter="*.algo")
        #add some method to send file name to backend here!!
        # print fileName 
        # """ADD FUNCTION HERE...LET IT RETURN TRUE IF VALID FILE"""
        # parser = Parser(None) # don't need a path to recipe
        # recipe = parser.parse_recipe(str(fileName[0]))
        # if recipe:
        #     self.table.addRecipe(recipe.name)
        self.controller.add_recipe(fileName)

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
        self.table.controller.remove_recipe(self.table.rowNums[self.row],self.row) # sends the name to the controller


class Table(QTableWidget):
    
    def __init__(self):
        super(Table, self).__init__(0, 5) #init with one row, 5 columns
        self.rows = {} # contains all of the rows
        self.rowNums = {}
        self.initgui()
        self.controller = None 
        
    def initgui(self):
        # add the headers
        headers = ["Recipe", "Value", "P/L", "% Return", "Remove?"]
        self.setHorizontalHeaderLabels(headers)  
        # add the total row
        self.rows['total'] = TotalRow(self,data={
            'value':0,
            'pli':0,
            'percent':0
            })
        self.verticalHeader().hide()
        
    def addRecipe(self, name,data={}):
        #TODO: add color!!!
        data = data or {
            'value':0,
            'pli':0,
            'percent':0
        }
       # self.setRowCount(self.rowCount() + 1)
        self.rows[name] = Row(self,name,data)

    def update(self,update_data):
        for name,data in update_data:
            self.rows[name].updateRow(data)

    def notifyRows(self, rowRemoved):
        for row in xrange(rowRemoved, self.rowCount()):
            button = self.cellWidget(row, 4)
            button.updateRow(button.row - 1)

class Row(object):
    """ models a row in the table """
    def __init__(self,table,name,data={}):
        self.name = name
        self.data = data
        self.table = table
        self.gui = {}
        # set the QT bullshit
        self.initgui()
        # set the formatting strings for updating
        self.formats = {
            'value' : (lambda x: '$'+x),
            'pli' : (lambda x: '$'+x),
            'percent': (lambda x: x+'%')
        }

    def initgui(self):
        rows = self.table.rowCount()
        #expand the table by one row
        self.table.setRowCount(rows + 1)
        self.table.rowNums[self.table.rowCount()] = self.name # set the name for removal
        #add name cell with checkbox
        self.gui['name'] = QTableWidgetItem(self.name)
        self.gui['name'].setCheckState(Qt.Checked)
        self.gui['name'].setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable)
        self.table.setItem(rows, 0, self.gui['name'])
        
        #set default values for other cells:
        self.gui['value'] = QTableWidgetItem("$0")
        self.gui['value'].setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table.setItem(rows, 1, self.gui['value'])
        ## PLI
        self.gui['pli'] = QTableWidgetItem("$0")
        self.gui['pli'].setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table.setItem(rows, 2, self.gui['pli'])
        ## Percent
        self.gui['percent'] = QTableWidgetItem("0%")
        self.gui['percent'].setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table.setItem(rows, 3, self.gui['percent'])       
        #add in remove button
        self.gui['remove'] = RemoveButton(self.table, rows)
        self.table.setCellWidget(rows, 4, self.gui['remove'])
    
    def updateRow(data):
        """
        data has the same variables as our gui:
        - value
        - PLI
        - percent
        """
        for key, value in data:
            self.gui[key].setText(self.formats[key](value)) # returns a formatted version of the data


class TotalRow(Row):
    """ subclass or row that just has GUI differences """
    def __init__(self,table,name="Total:",data={}):
        super(TotalRow,self).__init__(table,name,data)
        self.table.removeCellWidget(0,4) # remove the remove button :*
        self.gui['remove'] = QTableWidgetItem("")
        self.gui['remove'].setFlags(Qt.ItemIsEnabled)  
        self.table.setItem(0,4,self.gui['remove']) # no text there!
        for k,v in self.gui.iteritems():
            v.setBackground(QBrush(QColor("lightgray")))
            v.setFont(QFont("Arial", 15, QFont.Bold))

class Window(QWidget):
    
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, WINDOW_W, WINDOW_H)
        self.setWindowTitle("Recipes")
        table = Table()
        addButton = AddButton(table)
        print table.rows 
        
        layout = QVBoxLayout()
        layout.addWidget(table)
        layout.addWidget(addButton)        
        
        self.setLayout(layout)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())

