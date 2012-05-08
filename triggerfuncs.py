# trigger functions
##
import yfinance as yfinance

def test_oncall():
	print 'trigger called'
	return (10,1)  # every time it's triggered we get +10 shares

def get_price(ticker,d):
	print 'updating price'
	return yfinance.get_historical(ticker, d)

def buy_stock(ticker,amount,type,cash):
	"""
	ticker: stock ticker
	amount: quantity
	type: 'SHARES' or 'DOLLARS'
	"""
	value = yfinance.get_price(ticker)
	value = float(value)
	amount = int(amount)
	
	if type == 'DOLLARS':
		amount //= value
	if (amount*value) < cash[-1]:
		print 'you bought: ', value*amount 
		cash[-1] -= value*amount
		return (amount,value)
	return (1,1)

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
    
"""
Sell_stock and sell_short are identical
"""
def sell_short(ticker, amount, type, cash):
    return sell_stock(ticker, amount, type, cash);
	
