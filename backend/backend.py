# Backend code
#	CS032 Final Project - TradeUp
###
import json 

class Expression:
	"""
	Models an expression used when building a recipe.
	For example: represents a moving average.

	The GUI can simply have a reference to this.
	"""

	# attributes of the object
	self.func = None # the function used to evaluate the data
	self.type = self.func # type = func, but could be changed; e.g. you have one negated..?
	self.val = None # the value to be evaluated by the function

	def __init__(self):
		# TODO: override in subclass (assign attributes)

	def __eq__(self,other):
		return self.type == other.type


	def __setattr__(self,name,value):
		"""
		Modifies the standard attribute access so that changing .func updates
		type if they're already the same.
		"""
		if name is 'func' and self.func == self.type:
			self.__dict__['func'],self.__dict__['type'] = value,value

	# these are just for debugging
	def __unicode__(self):
		return u'Type: %s\nFunc: %s\nValue: %s\n' (unicode(self.type),unicode(self.func),unicode(self.val))
	# debugging... str() or %s
	def __str__(self):
		return 'Type: %s\nFunc: %s\nValue: %s\n' (unicode(self.type),unicode(self.func),unicode(self.val))

	# this is for saving the object to a file
	def json(self):
		return json.dumps(self.__dict__)

	def eval(self):
		# this is just a hacked ternary operator: index is evaluated first
		return (None,self.func(self.val))[(self.func and self.val)]

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
			'expr_a' : self.expr_a.__dict__,
			'expr_b' : self.expr_b.__dict__,
			'operator' : self.operator
		}
		return data

	def dump(self):
		return json.dumps(self.data())

	def eval(self):
		""" evaluates the row """
		if self.operator is ">":
			return (self.expr_a.eval() > self.expr_b.eval())
		elif self.operator is "<":
			return (self.expr_a.eval() < self.expr_b.eval())
		else
			return (self.expr_a.eval() == self.expr_b.eval()) 

	def __str__(self):
		# for debugging
		return "Expr A: %s\nExpr B: %s\nOperator: %s\n" (self.expr_a,self.expr_b,self.operator)


class Recipe:
	""" 
	Backend representation of a recipe. Used for saving the recipe to JSON. 
	"""


	def __init__(self):
		self.rows = []

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

	def to_file(self,file):
		"""this takes a file path"""
		with open(file) as output:
			output.write(self.json())


