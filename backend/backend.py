# Backend code
#	CS032 Final Project - TradeUp
###
import json 
import exprfuncs

class Expression:
	"""
	Models an expression used when building a recipe.
	For example: represents a moving average.

	The GUI can simply have a reference to this.
	"""

	# attributes of the object

	def __init__(self,func=None,val=None,typ=None):
		# TODO: override in subclass (assign attributes)
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
	def json(self):
		return json.dumps(self.data())
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

class RecipeRow:
	"""
	Models a row in the recipe, consists of:
		expr_a, operator, expr_b
	
		expr_a : Expression
		expr_b : Expression
		operator: String - ">","<" or "="/"==" 
	"""

	def __init__(self,a=None,b=None,c=None):
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

	def dump(self):
		return json.dumps(self.data())

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


class Recipe:
	""" 
	Backend representation of a recipe. Used for saving the recipe to JSON. 
	"""


	def __init__(self,trigger=None):
		self.rows = []
		self.trigger = trigger 

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

		return data

	def json(self):
		return json.dumps(self.data())

	def to_file(self,path):
		"""this takes a path """
		with open(path,'w') as output:
			output.write(self.json())

class Portfolio:
	
########
#### Parsing/Evaluating Code
########
class RowParse:
	"""
	Reads and parses a .algo file
	"""
	def __init__(self):
		self.data = {}

	def set_data(self,data):
		self.data = data 

	def expr_a(self):
		return Expression(func=getattr(exprfuncs,self.data['expr_a']['func']),
		val=self.data['expr_a']['val'])

	def expr_b(self):
		return Expression(func=getattr(exprfuncs,self.data['expr_b']['func']),
		val=self.data['expr_b']['val'])

	def operator(self):
		return self.data['operator']

	def getrow(self):
		return RecipeRow(a=self.expr_a(),b=self.expr_b(),c=self.operator())

class RecipeBuilder:

	def __init__(self,path):
		rowparser = RowParse()
		self.recipe = Recipe() 

		with open(path) as f:
			data = json.loads(f.read())
			for row in data:
				rowparser.set_data(row)
				self.recipe.add_row(rowparser.getrow())

class Evaluator:
	"""
	Evaluates a .algo file on every eval() 
	"""
	def __init__(self,path):
		rb = RecipeBuilder(path)
		self.recipe = rb.recipe 
		self.triggered = False 

	def eval(data):
		for row in self.recipe.rows:
			if(row.eval(data) and not self.triggered):
				if not self.triggered:
					self.recipe.trigger()
					self.triggered = True
				else:
					self.triggered = False 


