# Backend-tests:
#	procedural: unit tests for backend package code
####
import math
import exprfuncs
from backend import Expression, RecipeRow, Recipe,RecipeBuilder

def test_save(path):
	expr = Expression(func=getattr(exprfuncs,'expr_test_a'),val=8)

	expr_b = Expression(func=getattr(exprfuncs,'expr_test_b'),val=2)

	row = RecipeRow(a=expr,b=expr_b,c="=")

	assert (row.eval(2))

	recipe = Recipe()
	recipe.add_row(row)

	recipe.to_file(path)

def test_load(path):
	rb = RecipeBuilder(path)
	assert len(rb.recipe.rows) is 1 
	
	for row in rb.recipe.rows:
		assert(row.eval(2))

if __name__ == "__main__":
	test_save("test.algo")
	test_load("test.algo")
