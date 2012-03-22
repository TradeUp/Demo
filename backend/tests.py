# Backend-tests:
#	procedural: unit tests for backend package code
####
import math
import exprfuncs
from backend import Expression, RecipeRow, Recipe,RecipeBuilder

def expr_test_b(x):
	return x**x
def expr_test_a(x):
	return x**(0.5)

def test_save(path):
	expr = Expression(func=expr_test_a,val=16)

	expr_b = Expression(func=expr_test_b,val=2)

	row = RecipeRow(a=expr,b=expr_b,c="=")

	assert (row.eval())

	recipe = Recipe()
	recipe.add_row(row)

	recipe.to_file(path)

def test_load(path):
	rb = RecipeBuilder(path)
	assert len(rb.recipe.rows) is 1 
	
	for row in rb.recipe.rows:
		assert(row.eval())

if __name__ == "__main__":
	test_save("test.algo")
	test_load("test.algo")
