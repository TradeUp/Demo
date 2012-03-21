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


