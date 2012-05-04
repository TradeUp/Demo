#
# Expression Functions
##
import datetime,yfinance

def expr_test_b(x,d):
	return x*((d%2)+1) # starts with 5 
def expr_test_a(x,d):
	return x # starts with 10

def historical_price(ticker,date):
	""" takes a datetime.date and a string ticker"""
	return yfinance.get_historical(ticker,date)
