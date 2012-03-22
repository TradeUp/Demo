# Backend code
#	CS032 Final Project - TradeUp
###
import json 
import exprfuncs
import triggerfuncs

class BackendObj:
	def __init__(self,color=None):
		self.color = color or "red"
		self.performance = { self.color : []}

	def json(self):
		return json.dumps(self.data())

	def performance_update(self,point):
		point = point or 0
		self.performance[self.color].append((self.performance[self.color][-1]+point))
		return self.performance[self.color][-1] 

class Expression(BackendObj):
	"""
	Models an expression used when building a recipe.
	For example: represents a moving average.

	The GUI can simply have a reference to this.
	"""

	# attributes of the object

	def __init__(self,func=None,val=None,typ=None):
		# TODO: override in subclass (assign attributes)
		super(Expression).__init__(self)

		self.func = func
		self.val = val 
		self.typ = typ or func 

		def __eq__(self,other):
			return self.typ == other.typ



	# these are just for debugging
	def __unicode__(self):
		return u'typ: %s\nFunc: %s\nValue: %s\n' (unicode(self.typ),unicode(self.func),unicode(self.val))
	# debugging... str() or %s
	def __str__(self):
		return 'typ: %s\nFunc: %s\nValue: %s\n' (unicode(self.typ),unicode(self.func),unicode(self.val))

	# this is for saving the object to a file
	
	def data(self):
		return {
			'func': self.func.func_name,
			'val': self.val,
			'typ': self.typ.func_name
			}

	def eval(self,data):
		if self.func and self.val:
			return self.func(self.val,data)
		return None 

class RecipeRow(BackendObj):
	"""
	Models a row in the recipe, consists of:
		expr_a, operator, expr_b
	
		expr_a : Expression
		expr_b : Expression
		operator: String - ">","<" or "="/"==" 
	"""

	def __init__(self,a=None,b=None,c=None):
		super(RecipeRow).__init__(self)
		self.expr_a = a or None
		self.expr_b = b or None
		self.operator = c or None


	def __eq__(self,other):
		return (self.expr_a == other.expr_a) and (self.expr_b==other.expr_b) and (self.operator==other.operator)

	# returns a JSON dict of itself
	def data(self):
		data = {
			'expr_a' : self.expr_a.data(),
			'expr_b' : self.expr_b.data(),
			'operator' : self.operator
		}
		return data

	def eval(self,data):
		""" evaluates the row """
		if self.operator is ">":
			return (self.expr_a.eval(data) > self.expr_b.eval(data))
		elif self.operator is "<":
			return (self.expr_a.eval(data) < self.expr_b.eval(data))
		else:
			return (self.expr_a.eval(data) == self.expr_b.eval(data)) 

	def __str__(self):
		# for debugging
		return "Expr A: %s\nExpr B: %s\nOperator: %s\n" (self.expr_a,self.expr_b,self.operator)


class Recipe(BackendObj):
	""" 
	Backend representation of a recipe. Used for saving the recipe to JSON. 
	"""


	def __init__(self,trigger=None,color=None,rows=None):
		super(Recipe).__init__(self)
		self.rows = rows or []
		self.color = color or "green";
		self.trigger = trigger
		self.performance = { self.color : []} 

	def __eq__(self,other):
		# don't really knwo why I wrote this
		if not self.rows and other.rows: return False 
		for s,o in zip(self.rows,other.rows):
			if s is not o: return False 

	def add_row(self,row):
		self.rows.append(row)


	def data(self):
		data = []
		for row in self.rows:
			data.append(row.data())
		out = {
			'trigger' : self.trigger.data(),
			'rows' : data
		}
		return out

	def to_file(self,path):
		"""this takes a path """
		with open(path,'w') as output:
			output.write(self.json())

	def eval(self,data):
		""" evalutes against the piece of data, triggers trigger if appropriate. trigger will return data """
		run = 0
		for row in self.rows:

			point = None 
			if row.eval():
				point = self.trigger.activate()

			run += row.performance_update(point) # add it to the sum
		
		run /= len(self.rows)
		return self.performance_update(run)

class Portfolio(BackendObj):
	"""
	Represents a portfolio; a collection of recipes
	""" 
	def __init__(self,color=None):
		super(Portfolio).__init__(self)
		self.color = color or "red" # TODO: what kind of color data is needed here?
		self.recipes = []
		self.performance = { self.color : [] }

	def add_recipe(self,recipe):
		self.recipes.append(recipe)

	def eval(self,data):
		run = 0
		for recipe in self.recipes:
			run += recipe.eval()
		run /= len(self.recipes)

		return self.performance_update(run)

	def data(self):
		out = []
		for recipe in self.recipes:
			out.append(recipe.data())
		return out

	def to_file(self,path):
		with open(path,'w') as output:
			output.write(self.json())

#### The Trigger Class ####
#
# usage: 
#	during eval() or a row, trigger.activate() is called when conditions are true.
#	its our job to make sure this only happens when it's been reset before. (i.e in between calls)
#
###
class Trigger:

	def __init__(self,oncall=None):
		self.tripped = False 
		self.func = getattr(triggerfuncs,oncall) or (lambda: 1)
	
	def activate(self):
		if self.tripped:
			self.tripped = False
			return None 
		else:
			return self.func() # returns a positive or negative numebr representign the outcome 

	def data(self):
		return self.func.func_name
########
#### Parsing/Evaluating Code
########
class Parser:
	"""
	Reads and parses a .algo file
	"""
	def __init__(self,path):
		with open(path) as f:
			self.data = json.loads(f.read())
		"""
		self.data will be a list of recipes, which are a dict of: trigger, rows """

	def build_portfolio(self):
		""" returns a portfolio from the data """
		self.portfolio = Portfolio() # decide how you want to put in the color
		for recipe_data in self.data:
			rows = []
			for row in recipe_data['rows']:
				rows.append(self.getrow(row))
			self.portfolio.add_recipe(Recipe(trigger=Trigger(oncall=recipe_data['trigger']),rows=rows)) # you should add color here
		return self.portfolio

	def expr_a(self,data):
		return Expression(func=getattr(exprfuncs,data['expr_a']['func']),
		val=data['expr_a']['val'])

	def expr_b(self,data):
		return Expression(func=getattr(exprfuncs,data['expr_b']['func']),
		val=data['expr_b']['val'])

	def operator(self,data):
		return data['operator']

	def getrow(self,data):
		return RecipeRow(a=self.expr_a(data),b=self.expr_b(data),c=self.operator(data))


class Evaluator:
	"""
	Evaluates a .algo file on every eval() 
	"""
	def __init__(self,path):
		parser = Parser(path)
		self.portfolio = parser.build_portfolio()


	def eval(data):
		self.portfoliio.eval(data)


