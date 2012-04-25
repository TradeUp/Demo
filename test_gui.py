#
# tests of the gui combined with some 
# loading and saving
###
import math,sys
import exprfuncs
from backend import Expression, RecipeRow, Recipe,Portfolio, Parser,Trigger
from PySide.QtGui import QApplication
from SimpleTable import Window 

def create_recipe(path):
	expr = Expression(func=getattr(exprfuncs,'expr_test_a'),val=8)
	expr_b = Expression(func=getattr(exprfuncs,'expr_test_b'),val=2)
	row = RecipeRow(a=expr,b=expr_b,c="=")
	assert (row.eval(2))
	recipe = Recipe(trigger=Trigger(oncall='test_trigger_a'),name="Dylan")
	recipe.add_row(row)
	recipe.to_file(path) # save it to the path

def init_gui():
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())

if __name__ == "__main__":
	create_recipe("myrecipe.algo")
	init_gui()