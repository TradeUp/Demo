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
		res = yfinance.get_historical(tick,d)
		print 'result: ',res
		return res 
	else:
		return yfinance.get_price(tick)
	
def get_change(tick,d):
	return yfinance.get_change(tick)

def get_volume(tick,d):
	return yfinance.get_volume(tick)

def get_avg_daily_volume(tick,d):
	return yfinance.get_avg_daily_volume(tick)
def get_book_value(tick,d):
	return yfinance.get_book_value(tick)
def get_ebitda(tick,d):
	return yfinance.get_ebitda(tick)
def get_dividend_yield(tick,d):
	return yfinance.get_dividend_yield(tick)
def get_dividend_per_share(tick,d):
	return yfinance.get_dividend_per_share(tick)
def get_earnings_per_share(tick,d):
	return yfinance.get_earnings_per_share(tick)
def get_52_week_high(tick,d):
	return yfinance.get_52_week_high(tick)
def get_52_week_low(tick,d):
	return yfinance.get_52_week_low(tick)
def get_50day_moving_avg(tick,d):
	return yfinance.get_50day_moving_avg(tick)
def get_200day_moving_avg(tick,d):
	return yfinance.get_200day_moving_avg(tick)
def get_price_earnings_ratio(tick,d):
	return yfinance.get_price_earnings_growth_ratio(tick)
def get_price_earnings_growth_ratio(tick,d):
	return yfinance.get_price_earnings_growth_ratio(tick)
def get_price_sales_ratio(tick,d):
	return yfinance.get_price_sales_ratio(tick)
def get_price_book_ratio(tick,d):
	return yfinance.get_price_book_ratio(tick)
def get_short_ratio(tick,d):
	return yfinance.get_short_ratio(tick)
def get_market_cap(tick,d):
	""" this is an example, only supported in realtime """
	return yfinance.get_market_cap(tick)

#### Set up attributes
def exprfunc_data():
	return {
		'expr_test_b':'ALL',
		'expr_test_a':'ALL',
		'get_price_expr':'ALL',
		'get_market_cap':'REALTIME',
		'get_change':'REALTIME',
		'get_volume':'REALTIME',
		'get_avg_daily_volume':'REALTIME',
		'get_book_value':'REALTIME',
		'get_ebitda':'REALTIME',
		'get_dividend_per_share':'REALTIME',
		'get_dividend_yield':'REALTIME',
		'get_earnings_per_share':'REALTIME',
		'get_52_week_high':'REALTIME',
		'get_52_week_low':'REALTIME',
		'get_50day_moving_avg':'REALTIME',
		'get_200day_moving_avg':'REALTIME',
		'get_price_earnings_ratio':'REALTIME',
		'get_price_sales_ratio':'REALTIME',
		'get_price_book_price':'REALTIME',
		'get_short_ratio':'REALTIME'
	}
