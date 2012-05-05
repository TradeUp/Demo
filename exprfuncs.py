#
# Expression Functions
##
import datetime, yfinance as yfinance

def expr_test_b(x,d):
	return x*((d%2)+1) # starts with 5 
def expr_test_a(x,d):
	return x # starts with 10

def get_price_expr(tick,d):
	if isinstance(d,datetime.date):
		return yfinance.get_historical(tick,d)
	else:
		return yfinance.get_price(tick)
	
def get_market_cap(tick,d):
	""" this is an example, only supported in realtime """
	return yfinance.get_market_cap(tick)

#### Set up attributes
def exprfunc_data():
	return {
		'expr_test_b':'ALL',
		'expr_test_a':'ALL',
		'get_price_expr':'REALTIME',
		'get_market_cap':'REALTIME'
	}
