# trigger functions
##
import yfinance as yfinance

def test_oncall():
	print 'trigger called'
	return (10,1)  # every time it's triggered we get +10 shares

def test_getPrice(data):
	return 1 # price stays constant


def buy_stock(ticker,amount,type,cash):
	"""
	ticker: stock ticker
	amount: quantity
	type: 'SHARES' or 'DOLLARS'
	"""
	value = yfinance.get_price(ticker)
	if type == 'DOLLARS':
		amount //= value

	cash[-1] -= value*amount
	return (amount,value)

def sell_stock(ticker,amount,type,cash):
	"""
	ticker: stock symbol
	amount: quantity
	type: 'SHARES' or 'DOLLARS'
	this is also used for selling short
	"""
	value = yfinance.get_price(ticker)

	if type == 'DOLLARS':
		amount //= value # you can only sell amount many shares

	cash[-1] += value*amount 
	return (-amount,value) # you sold it dingus!
	
