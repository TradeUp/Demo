# Backend-tests:
#	procedural: unit tests for backend package code
####
import math
import exprfuncs
from backend import Expression, RecipeRow, Recipe,Portfolio, Parser,Trigger

def test_save(path):
	expr = Expression(func=getattr(exprfuncs,'expr_test_a'),val=8)

	expr_b = Expression(func=getattr(exprfuncs,'expr_test_b'),val=2)

	row = RecipeRow(a=expr,b=expr_b,c="=")

	assert (row.eval(2))

	recipe = Recipe(trigger=Trigger(oncall='test_trigger_a'))
	recipe.add_row(row)
	# portfolio
	portfolio = Portfolio()
	portfolio.add_recipe(recipe)
	portfolio.to_file(path)

def test_load(path):
	parser = Parser(path)
	portfolio = parser.build_portfolio()

	assert(portfolio)
	assert(len(portfolio.recipes)==1)
	assert(len(portfolio.recipes[0].rows)==1)
	print portfolio.eval(2) # 99
	print portfolio.eval(2) # 99
	print portfolio.eval(1) # 99
	print portfolio.eval(2) # 98
	print portfolio.eval(2) # 98 
	print portfolio.get_performance()

if __name__ == "__main__":
	test_save("test.algo")
	test_load("test.algo")
