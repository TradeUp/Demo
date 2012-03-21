#Readme
####C-Level Demo Code: TradeUp

## Description
This contains the code for our c-level demo of our application, an algorithmic trading simulator. 

## Backend
###Expression
This class models an expression (e.g. price('IBM')).
###RecipeRow
A row in a recipe. Contains:
	
* two expressions
* an operator (">","<", or "=")

A row can be evaluated to return a boolean value using the eval() function.
###Recipe
Represents a complete recipe; basically just a wrapper around a list of rows. Provides a json() function as well as to_file. Use:

	path = "/usr/apps/tradeup/recipes/new_recipe.algo"
	my_recipe.to_file(path)

That was probably a completely pointless usage example.

###RowParse
This class parses one row of data in an algo file. It's passed a dictionary (data) by a recipebuilder.

TODO:

* is setting set_data really the best method here?

###RecipeBuilder
Builds a recipe object from a given filepath (to an algo file).
Access the recipe by recipebuilder.recipe

###Evaluator
Not complete (as of this commit). Evaluates a recipe. This should be called every time you look at a piece of data.
