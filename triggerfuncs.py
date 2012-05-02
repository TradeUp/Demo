# trigger functions
##
import yfinance

def test_oncall():
	print 'trigger called'
	return (10,1)  # every time it's triggered we get +10 shares

def test_getPrice(data):
	return 1 # price stays constant


def buy_stock(ticker,amount,type):
	"""
	ticker: stock ticker
	amount: quantity
	type: 'SHARES' or 'DOLLARS'
	"""
	value = yfinance.get_price(ticker)
	if type == 'SHARES': return (amount,value)
	amount //= value # you can only buy full shares of stock!
	return (amount,value)

def sell_stock(ticker,amount,type):
	"""
	ticker: stock symbol
	amount: quantity
	type: 'SHARES' or 'DOLLARS'
	"""
	value = yfinance.get_price(ticker)
	