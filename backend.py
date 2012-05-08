# Backend code
#	CS032 Final Project - TradeUp
###
import json,threading
import exprfuncs
import triggerfuncs
import datetime,yfinance,time 
from PySide import QtGui


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
		self.performance[self.color].append((quantity,float(new_price)))

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
		self.performance[self.color][-1] = (point[0]+quantity,float(price)) # add the change
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
		func_data = getattr(exprfuncs,'exprfunc_data')
		self.func = getattr(exprfuncs,func)
		self.funcName = func
		self.val = val 
		self.status = func_data()[func]
		




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

	def __init__(self,a,b,c):
		self.expr_a = a
		self.expr_b = b
		self.operator = c
		self.status = 'REALTIME' if (self.expr_a.status == 'REALTIME' or self.expr_b.status == 'REALTIME') else 'ALL'
			

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
		a = self.expr_a.run(data)
		b = self.expr_b.run(data)
		print self.operator 
		
		if self.operator == ">":
			print 'a: ', a ,' b:', b
			return (a > b)
		elif self.operator == "<":
			print 'a: ', a ,' b:', b
			return (a < b)
		else:
			return (a == b) 

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
		self.status = 'ALL'
		for r in self.rows:
			if r.status == 'REALTIME': self.status = 'REALTIME'
		

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
		self.update_value(self.trigger.get_price(self.trigger.ticker,data)) # gets the most recent price
		for row in self.rows:
			if not row.run(data):
				self.trigger.reset() 
				print 'not triggered'
				return self.last_point()
		new_val = self.trigger.activate(cash)
		print 'trigger activated, new value: ',new_val
		if new_val: self.first += new_val[1]*new_val[0] # add the amnt of money spent
		return self.performance_update(new_val)

class Portfolio(BackendObj):
	"""
	Represents a portfolio; a collection of recipes
	""" 
	def __init__(self,color="red",cash=10000):
		super(Portfolio,self).__init__(color)
		self.recipes = {}
		self.cash = [cash]

	def add_recipe(self,recipe):
		self.recipes[recipe.name] = recipe

	def remove_recipe(self,recipe):
		self.recipes[recipe] = None 

	def run(self,data):
		run_a,run_b = 0,0
		self.cash.append(self.cash[-1]) # copy the last value 
		for recipe in self.recipes.values():
			print 'this is what ur working with: ',recipe
			a = recipe.run(self.cash,data)
			print 'output: (a) ',a 
			run_a += int(a[0])
			run_b += float(a[1])
			# nice
		return self.add_point((run_a,run_b))

	def checkRun(self):
		for r in self.recipes.values():
			if r.run == 'REALTIME': return False 
		return True 
	
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

	def __init__(self,ticker,amount,amount_type,oncall):
		self.tripped = False 
		self.funcName = oncall
		self.func = getattr(triggerfuncs,oncall) or (lambda: 1)
		self.get_price = getattr(triggerfuncs,'get_price') or (lambda: 1)
		
		self.ticker = str(ticker)
		self.amount = int(amount)
		self.amount_type = str(amount_type)
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
			'getPrice': self.get_price.func_name,
			'amount':self.amount,
			'amount_type':self.amount_type,
			'ticker': self.ticker
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
			self.portfolio.add_recipe(Recipe(trigger=Trigger(oncall=recipe_data['trigger']['oncall'],amount=recipe_data['trigger']['amount'],amount_type=recipe_data['trigger']['amount_type'],ticker=recipe_data['trigger']['ticker']),rows=rows)) # you should add color here
		return self.portfolio

	def parse_recipe(self,path):
		""" returns a recipe from the specified path"""
		with open(path) as f:
			self.data = json.loads(f.read())
			if not self.data: return None 
			# build the recipe from the data
			rows = []
			print 'whats in here ',self.data
			for row in self.data['rows']:
				rows.append(self.getrow(row))
			return Recipe(trigger=Trigger(oncall=self.data['trigger']['oncall'],amount=self.data['trigger']['amount'],amount_type=self.data['trigger']['amount_type'],ticker=self.data['trigger']['ticker']),rows=rows,name=self.data['name'])


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
		self.graphed = ['cash']
		self.portfolio = Portfolio() 
		self.graph_axis = [] # reset for each run
		self.graph_output = {}
		self.table_output = {}
		self.realtime = None 
		self.progress = None # progressbar
		self.unusedColors = ['b', 'r','c','m','y','k']
		self.usedColors = []
		self.running = False

	def add_recipe(self,filename):	
		recipe = None
		try:
			recipe = self.parser.parse_recipe(str(filename[0]))
		except:
			return None
		if(len(self.unusedColors) >= 1):
				recipe.color = self.unusedColors[0]
				self.usedColors.append(self.unusedColors[0])
				del self.unusedColors[0]
		if recipe.name in self.portfolio.recipes: return 
		self.graphed.append(recipe.name)
		if recipe:
			self.table.addRecipe(recipe.name) #TODO: add data also
			self.portfolio.add_recipe(recipe)
			# self.graph.add_recipe(recipe)
			
		return recipe
	def activate(self,recipeName):
		print recipeName, ' check it out'
		if recipeName not in self.graphed:
			self.graphed.append(recipeName)
			if(len(self.unusedColors) >= 1):
				self.portfolio.recipes.get(recipeName).color = self.unusedColors[0]
				self.usedColors.append(self.unusedColors[0])
				del self.unusedColors[0]
			self.refresh_graph()
	
	def deactivate(self,recipeName):
		print recipeName, 'hey my'
		if recipeName in self.graphed:
			self.graphed.remove(recipeName)
			self.unusedColors.append(self.portfolio.recipes.get(recipeName).color)
			self.refresh_graph()
			
	def remove_recipe(self,recipeName,rowNum):
		""" see above"""
		if self.running: return 
		self.portfolio.remove_recipe(recipeName)
		self.table.removeRow(rowNum)
		self.table.notifyRows(rowNum)
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
		if date == 'realtime':
			self.graph_axis.append(datetime.datetime.now())
		else:
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
				graph_output[recipe.name] = (graph_data,self.graph_axis,recipe.color)
			table_output[recipe.name] = result 
		# send the output to the table
		if 'cash' in self.graphed:
			graph_output['cash'] = (self.portfolio.cash,self.graph_axis, 'g') 
			table_output['cash'] = {
										'value': self.portfolio.cash[-1],
										'pli': (self.portfolio.cash[-1] - self.portfolio.cash[0]),
										'percent': ((self.portfolio.cash[-1] - self.portfolio.cash[0]) / self.portfolio.cash[0])
									}
		self.graph_output = graph_output # we always know the last output
		self.table_output = table_output 
		
	def refresh_graph(self):
		print 'calling refresh graph for some reason'
		data = {}
		for recipeName in self.graphed:
			data[recipeName] = self.graph_output[recipeName]
		self.graph.refresh(data)
	##
	# methods to be called on the GUI side
	#
	def run_historical(self,start,end):
		""" takes two datetime.dates """
		self.reset()
		if not self.portfolio.checkRun():
			error = QtGui.QErrorMessage()
			error.showMessage('Error: Recipe uses Expressions Unsupported in historical data. Please run real-time.')
			error.exec_()
			return 
			
		## progress bar
		diff = end - start
		count = int((diff.total_seconds()) / 86400)
		begin = 0
		
		self.progress.setRange(0,count)
		self.progress.setVisible(True)
		
		self.graph_axis = [start] # reset the axis

#		curr = start;
#		day = datetime.timedelta(days=1) # to add a day
#		end += day 
#
#		while(not same_date(curr,end)):
#			self.progress.setValue(begin)
#			self.run(curr)
#			curr += day 
#			begin += 1

		thre = HstoryThread(self,start,end)
		thre.start()
			
#		self.graph.update(self.graph_output,self.table,self.table_output);

	
	def validate_ticker(self,ticker):
		""" validates a ticker symbol by trying a request to Yahoo
		"""
		if ticker == "" or yfinance.get_price(ticker) == '0.00':
			return False
		return True 
	
	def validate_trigger(self,ticker,amount,amount_type,oncall,getPrice):
		""" trigger validation method """
		if not self.validate_ticker(ticker): return False
		if amount < 0: return False
		if amount_type != 'SHARES' and amount_type != 'DOLLARS': return False
		if not getattr(triggerfuncs,oncall) or not getattr(triggerfuncs,getPrice): return False
		return True 
	
	def reset(self):
		self.graph_output = {}
		self.table_ouput = {}
		self.graph_axis = []
		self.portfolio.cash = [self.portfolio.cash[0]]
		for k,recipe in self.portfolio.recipes.items():
			recipe.performance = { recipe.color : [(0,0)]}
			recipe.trigger.reset()
		self.portfolio.performance = { self.portfolio.color : [(0,0)] }

	def run_realtime(self):
		""" runs a realtime simulation (until you call stop_realtime)
		"""
		self.reset()
		# for the default
		self.progress.setVisible(False)
		self.progress.setRange(0,100)
		curr = datetime.datetime.now()
		self.graph_axis = [curr]
		
		try:
			self.realtime = RealThread(0,self)
			self.realtime.start()
		except  Exception as e:
			print 'Error. unable to thread ', e

	def stop_realtime(self):
		""" called to stop the realtime run"""
		self.running = False 
		self.realtime.stop()
		self.graph.update(self.graph_output,self.table,self.table_output);

class HstoryThread(threading.Thread):
	def __init__(self,parent,s,end):
		super(HstoryThread,self).__init__()
		self.parent = parent
		self.s = s
		self.end = end
		
	def stop(self):
		pass 	
	def run(self):
		self.parent.running = True 
		curr = self.s;
		day = datetime.timedelta(days=1) # to add a day
		self.end += day 
		begin = 0
		
		while(not same_date(curr,self.end)):
			self.parent.progress.setValue(begin)
			self.parent.run(curr)
			curr += day 
			begin += 1
			self.parent.graph.update(self.parent.graph_output,self.parent.table,self.parent.table_output,self.parent.color);
		self.join()
		self.parent.running = False 

class RealThread(threading.Thread):
	def __init__(self,ID,parent):
		super(RealThread,self).__init__()
		self.ID = ID
		self.parent = parent
		self.end = threading.Event()
	def stop(self):
		self.end.set()
	def run(self):
		self.parent.running = True 
		count = 0
		while not self.end.isSet():
			print 'runnign: ',self.parent
			self.parent.progress.setValue(count)
			self.parent.run('realtime')
			count +=1
			time.sleep(2)
			self.parent.graph.update(self.parent.graph_output,self.parent.table,self.parent.table_output);

