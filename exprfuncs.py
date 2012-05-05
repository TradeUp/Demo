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