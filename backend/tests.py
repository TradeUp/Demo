# Backend-tests:
#	procedural: unit tests for backend package code
####
import math
from backend import Expression, RecipeRow, Recipe

def expr_test_b(x):
	return x**x
def expr_test_a(x):
	return x**(0.5)

def test():
	expr = Expression(func=expr_test_a,val=16)

	expr_b = Expression(func=expr_test_b,val=2)

	row = RecipeRow(a=expr,b=expr_b,c="=")

	assert (row.eval())

	recipe = Recipe()
	recipe.add_row(row)

	print recipe.json()

if __name__ == "__main__":
	test() 
