# Backend code
#	CS032 Final Project - TradeUp
###
import json
import exprfuncs
import triggerfuncs
import datetime,yfinance,time 

def same_date(a,b):
	if a.day == b.day:
		if a.month == b.month:
			return a.year == b.year 

class BackendObj(object):
	def __init__(self,color):
		self.color = color
		self.first = 0 
		self.performance = { self.color : [(0,0)]} # decide initial amount of portfolio
	def json(self):
		return json.dumps(self.data())

	def update_value(self,new_price):
		quantity,price = self.performance[self.color][-1] # get last tuple
		self.performance[self.color].append((quantity,new_price))

	def last_point(self):
		print self.performance[self.color]
		return self.performance[self.color][-1]
	def add_point(self,point):
		self.performance[self.color][-1] = point 
		return self.performance[self.color][-1]

	def performance_update(self,point):
		""" triggered when your trigger goes off """
		if not point:
			print 'no change'
			return self.last_point()
		quantity, price = self.performance[self.color][-1]
		self.performance[self.color][-1] = (point[0]+quantity,price) # add the change
		return self.performance[self.color][-1] 

	def get_performance(self):
		return self.performance[self.color]

class Expression:
	"""
	Models an expression used when building a recipe.
	For example: represents a moving average.

	The GUI can simply have a reference to this.
	"""

	# attributes of the object

	def __init__(self,func=None,val=None,typ=None):
		# TODO: override in subclass (assign attributes)
		self.func = getattr(exprfuncs,func)
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
			'val': self.val     
			}

	def run(self,data):
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
	def json(self):
		return json.dumps(self.data())

	# returns a JSON dict of itself
	def data(self):
		data = {
			'expr_a' : self.expr_a.data(),
			'expr_b' : self.expr_b.data(),
			'operator' : self.operator
		}
		return data

	def run(self,data):
		""" evaluates the row """
		if self.operator is ">":
			return (self.expr_a.run(data) > self.expr_b.run(data))
		elif self.operator is "<":
			return (self.expr_a.run(data) < self.expr_b.run(data))
		else:
			return (self.expr_a.run(data) == self.expr_b.run(data)) 

	def __str__(self):
		# for debugging
		return "Expr A: %s\nExpr B: %s\nOperator: %s\n" (self.expr_a,self.expr_b,self.operator)


class Recipe(BackendObj):
	""" 
	Backend representation of a recipe. Used for saving the recipe to JSON. 
	"""


	def __init__(self,trigger=None,color="green",rows=[],name="Default"):
		super(Recipe,self).__init__(color)
		self.rows = rows
		self.trigger = trigger
		self.name = name

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
			'rows' : data,
			'name' : self.name
		}
		return out

	def to_file(self,path):
		"""this takes a path """
		with open(path,'w') as output:
			output.write(self.json())

	def run(self,cash,data):
		""" evalutes against the piece of data, triggers trigger if appropriate. trigger will return data """
		self.update_value(self.trigger.get_price(data)) # gets the most recent price
		for row in self.rows:
			if not row.run(data):
				self.trigger.reset() 
				return self.last_point()
		new_val = self.trigger.activate(cash)
		print 'trigger activated, new value: ',new_val
		if new_val: self.first += new_val[1]*new_val[0] # add the amnt of money spent
		return self.performance_update(new_val)

class Portfolio(BackendObj):
	"""
	Represents a portfolio; a collection of recipes
	""" 
	def __init__(self,color="red",cash="10000"):
		super(Portfolio,self).__init__(color)
		self.recipes = {}
		self.cash = [cash]

	def add_recipe(self,recipe):
		self.recipes[recipe.name] = recipe

	def remove_recipe(self,recipe):
		self.recipes[recipe.name] = None 

	def run(self,data):
		run_a,run_b = 0,0
		self.cash.append(self.cash[-1]) # copy the last value 
		for recipe in self.recipes.values():
			a = recipe.run(self.cash,data)
			print a
			run_a += a[0]
			run_b += a[1]
			# nice
		return self.add_point((run_a,run_b))

	def data(self):
		out = []
		for key, recipe in self.recipes.items():
			out.append(recipe.data())
		return out

	def to_file(self,path):
		with open(path,'w') as output:
			output.write(self.json())

#### The Trigger Class ####
#
# usage: 
#	during run() or a row, trigger.activate() is called when conditions are true.
#	its our job to make sure this only happens when it's been reset before. (i.e in between calls)
#
###
class Trigger:

	def __init__(self,ticker,amount,amount_type,oncall,getPrice):
		self.tripped = False 
		self.func = getattr(triggerfuncs,oncall) or (lambda: 1)
		self.get_price = getattr(triggerfuncs,getPrice) or (lambda: 1)
		
		self.ticker = ticker
		self.amount = amount
		self.amount_type = amount_type
		self.running = False 
		
	def activate(self,cash):
		if self.tripped:
			return None 
		else:
			self.tripped = True 
			print 'activating trigger: ',self.func.func_name
			return self.func(self.ticker,self.amount,self.amount_type,cash) # returns a positive or negative numebr representign the outcome 

	def reset(self):
		self.tripped = False 
		return None 

	def data(self):
		return {
			'oncall': self.func.func_name,
			'getPrice': self.get_price.func_name
			}
########
#### Parsing/Evaluating Code
########
class Parser:
	"""
	Reads and parses a .algo file
	"""
	def __init__(self,path):
		if path:
			with open(path) as f:
				self.data = json.loads(f.read())
				print self.data 
		"""
		self.data will be a list of recipes, which are a dict of: trigger, rows """

	def build_portfolio(self):
		""" returns a portfolio from the data """
		self.portfolio = Portfolio() # decide how you want to put in the color
		for recipe_data in self.data:
			rows = []
			for row in recipe_data['rows']:
				print 'parsing row: ', row
				rows.append(self.getrow(row))
			self.portfolio.add_recipe(Recipe(trigger=Trigger(oncall=recipe_data['trigger']['oncall'],getPrice=recipe_data['trigger']['getPrice']),rows=rows)) # you should add color here
		return self.portfolio

	def parse_recipe(self,path):
		""" returns a recipe from the specified path"""
		with open(path) as f:
			self.data = json.loads(f.read())
			if not self.data: return None 
			# build the recipe from the data
			rows = []
			for row in self.data['rows']:
				rows.append(self.getrow(row))
			return Recipe(trigger=Trigger(oncall=self.data['trigger']),rows=rows,name=self.data['name'])


	def expr_a(self,data):
		print 'expr a: ',data['expr_a']['func']
		return Expression(func=str(data['expr_a']['func']),
		val=data['expr_a']['val'])

	def expr_b(self,data):
		print data
		return Expression(func=str(data['expr_b']['func']),
		val=data['expr_b']['val'])

	def operator(self,data):
		return data['operator']

	def getrow(self,data):
		return RecipeRow(a=self.expr_a(data),b=self.expr_b(data),c=self.operator(data))


####
# Controller
#	updates the graph & table, receives drop/adds for recipes from the table
##
class Controller:

	def __init__(self,table,graph):
		self.table = table
		#table.controller = self
		self.graph = graph
		self.parser = Parser(None)
		self.graphed = []
		self.portfolio = Portfolio() 
		self.graph_axis = [] # reset for each run

	def add_recipe(self,filename):	
		recipe = self.parser.parse_recipe(str(filename[0]))
		if recipe:
			self.table.addRecipe(recipe.name) #TODO: add data also
			self.portfolio.add_recipe(recipe)
			# self.graph.add_recipe(recipe)

	def remove_recipe(self,recipeName,rowNum):
		""" see above"""
		self.portfolio.remove_recipe(recipeName)
		self.table.removeRow(self.row,rowNum)
		self.table.notifyRows(self.row,rowNum)
		# update the graph
		# self.graph.add_recipe(recipe)

	def add_recipe_graph(self,recipeName):
		self.graphed.append(recipeName)

	def remove_recipe_graph(self,recipeName):
		self.graphed.remove(recipeName)

	def pl_calc(self,recipe):
		l_quan,l_val = recipe.last_point()
		# multiply/subtract
		print 'recipe first: ',recipe.first
		return (l_quan*l_val - recipe.first)

	def per_calc(self,recipe,pl):
		if not recipe.first: return 0 
		return (pl/recipe.first)

	def run(self,date):
		"""
		note that date is of form: datetime.date
		"""
		self.graph_axis.append(date)
		table_output = {}
		graph_output = {}

		self.portfolio.run(date)

		for key,recipe in self.portfolio.recipes.items():
			# create a data object out of the recipe
			l_v,l_p = recipe.last_point()
			pl = self.pl_calc(recipe)
			result = {
				'value' : (l_v*l_p),
				'pli' : pl,
				'percent' : self.per_calc(recipe,pl)
			}
			if recipe.name in self.graphed:
				graph_data = [x*y for x,y in recipe.get_performance()]
				graph_output[recipe.name] = (graph_data,self.graph_axis)
			table_output[recipe.name] = result 
		# send the output to the table
		graph_output['cash'] = (self.portfolio.cash,self.graph_axis) 
		self.graph.update(graph_output,self.table,table_output);

	##
	# methods to be called on the GUI side
	#
	def run_historical(self,start,end):
		""" takes two datetime.dates """
		self.graph_axis = [] # reset the axis

		curr = start;
		day = datetime.timedelta(days=1) # to add a day
		end += day 

		while(not same_date(curr,end)):
			self.run(curr)
			curr += day 
	
	def validate_ticker(self,ticker):
		""" validates a ticker symbol by trying a request to Yahoo
		"""
		if yfinance.get_price(ticker) == '0.00':
			return False
		return True 
	
	def validate_trigger(self,ticker,amount,amount_type,oncall,getPrice):
		""" trigger validation method """
		if not self.validate_ticker(ticker): return False
		if amount < 0: return False
		if amount_type != 'SHARES' and amount_type != 'DOLLARS': return False
		if not getattr('triggerFuncs',oncall) or not getattr('triggerFuncs',getPrice): return False
		return True 
	
	def run_realtime(self):
		""" runs a realtime simulation (until you call stop_realtime)
		"""
		while(self.running):
			curr = datetime.datetime.now()
			self.graph_axis.append(curr)
			self.run(curr)
			time.sleep(10)
			
	def stop_realtime(self):
		""" called to stop the realtime run"""
		self.running = False 
		
		
		