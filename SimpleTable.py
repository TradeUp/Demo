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
        self.setText("add")
        self.setFixedSize(ADD_BUTTON_W, ADD_BUTTON_H)
        self.clicked.connect(self.chooseFile)
        self.controller = table.controller
        self.setStyleSheet('QPushButton { border-radius: 25px; } QPushButton:hover { color: #444; text-decoration: underline } ')
        
    def chooseFile(self):
        fileName = QFileDialog.getOpenFileName(self, dir="/home/dylan/mock_algo/", filter="*.algo")
        #add some method to send file name to backend here!!
        # print fileName 
        # """ADD FUNCTION HERE...LET IT RETURN TRUE IF VALID FILE"""
        # parser = Parser(None) # don't need a path to recipe
        # recipe = parser.parse_recipe(str(fileName[0]))
        # if recipe:
        #     self.table.addRecipe(recipe.name)
        if not fileName[0] == '': 
            recipe = self.controller.add_recipe(fileName)
            
            if not recipe:
                msgBox = QMessageBox(QMessageBox.Icon.Critical, "Error", "");
                msgBox.setText("Unable to open file.")
                msgBox.exec_()
                return

class RemoveButton(QPushButton):
    
    def __init__(self, table, row):
        super(RemoveButton, self).__init__()
        self.setIcon(QPixmap('remove.png')) 
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
        self.portfolioPath = None
        self.running = False
        self.cellClicked.connect(self.cellActive)
#        self.setFixedWidth(504)
        self.setMinimumHeight(100)
        
        for i in range(5):
            self.setColumnWidth(i,275)
    def cellActive(self,row,col):
        """ called when a cell is activated """
        if(col==0):
            if(self.item(row,col).checkState()):
                self.activateRecipe(self.item(row,col).text())
            else:
                self.deactivateRecipe(self.item(row,col).text())

    def activateRecipe(self,recipe):
        if 'Cash' in recipe: 
            recipe = 'cash'
        # call controller.activate on the row
        self.controller.activate(recipe)
    
    def deactivateRecipe(self,recipe):
        if 'Cash' in recipe: 
            recipe = 'cash'
        self.controller.deactivate(recipe)
    
    
    def initgui(self):
        # add the headers
        headers = ["Recipe", "Value", "P/L", "% Return", "Remove?"]
        self.setHorizontalHeaderLabels(headers)  
        # add the total row
        self.rows['cash'] = TotalRow(self,data={
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
        for name,data in update_data.items():
            self.rows[name].updateRow(data)

    def notifyRows(self, rowRemoved):
        for row in xrange(rowRemoved, self.rowCount()):
            button = self.cellWidget(row, 4)
            button.updateRow(button.row - 1)
    
    def savePortfolio(self):
        if self.portfolioPath == None:
            self.savePortfolioAs()
            return
        
        self.controller.portfolio.to_file(self.portfolioPath)
        
    def savePortfolioAs(self):
        #bring up a file dialog so they can open it
        path = QFileDialog.getSaveFileName(self, dir="/home/dylan/mock_algo/", filter="*.torg")[0]
        if path == '':
            return
        
        self.portfolioPath = path;
        
        self.savePortfolio()
    
    def openPortfolio(self):
        #bring up a file dialog so they can open it
        path = QFileDialog.getOpenFileName(self, dir="/home/dylan/mock_algo/", filter="*.torg")[0]
        if path == '':
            return
        
        self.portfolioPath = path
        
        parser = Parser(self.portfolioPath)
        self.controller.portfolio = parser.build_portfolio()
        
        #reset the rows and add all the new recipes
        self.rows = {}
        for key, recipe in self.controller.portfolio.recipes.items():
            self.addRecipe(recipe.name)

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
            'value' : (lambda x: '$'+str(x)),
            'pli' : (lambda x: '$'+str(x)),
            'percent': (lambda x: str(x) +'%')
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
        self.gui['name']
        
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
        
    
    def updateRow(self, data):
        """
        data has the same variables as our gui:
        - value
        - PLI
        - percent
        """
        for key, value in data.items():
            self.gui[key].setText(self.formats[key](value)) # returns a formatted version of the data


class TotalRow(Row):
    """ subclass or row that just has GUI differences """
    def __init__(self,table,name="Cash:",data={}):
        super(TotalRow,self).__init__(table,name,data)
        self.table.removeCellWidget(0,4) # remove the remove button :*
        self.gui['remove'] = QTableWidgetItem("")
        self.gui['remove'].setFlags(Qt.ItemIsEnabled)  
        self.table.setItem(0,4,self.gui['remove']) # no text there!
        for k,v in self.gui.iteritems():
            v.setBackground(QBrush(QColor("lightgray")))
            v.setFont(QFont("Arial", 15, QFont.Bold))

#class Window(QWidget):
#    
#    def __init__(self):
#        super(Window, self).__init__()
#        self.setGeometry(50, 50, WINDOW_W, WINDOW_H)
#        self.setWindowTitle("Recipes")
#        table = Table()
#        addButton = AddButton(table)
#        print table.rows 
#        
#        layout = QVBoxLayout()
#        layout.addWidget(table)
#        layout.addWidget(addButton)        
#        
#        self.setLayout(layout)
#        self.show()
#
#
#if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    w = Window()
#    sys.exit(app.exec_())

