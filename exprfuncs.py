#
# Expression Functions
##
import datetime, yfinance as yfinance
import math

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
	"""print d
	print str(isinstance(d, datetime.date))"""
	mktcap = yfinance.get_market_cap(tick)
	'''print "MKT CAP is " + str(mktcap)'''
	""" this is an example, only supported in realtime """
	return mktcap




def mean(tick, d, days=10.0):
	end = datetime.date.today()
	price_sum = 0.0
	for i in xrange(1,int(days) + 1):
		price_sum += float(get_price_expr(tick, end - datetime.timedelta(i))) 
	return price_sum/days

def mean_10_day(tick,d): 
	return mean(tick, d, 10.0)
	
def mean_30_day(tick,d): 
	return mean(tick, d, 30.0)



def std_dev(tick,d,days=10.0):
	return math.sqrt(variance(tick,d,days))

def std_dev_10_days(tick,d):
	return std_dev(tick,d,10.0)

def std_dev_30_days(tick,d):
	return std_dev(tick,d,30.0)






def variance(tick, d, days=10.0):
	end = datetime.date.today()
	summand = 0.0
	the_mean = mean(tick, d, days)
	sum_squares = 0.0
	for i in xrange(1, int(days) + 1): 
		price = float(get_price_expr(tick, end - datetime.timedelta(i)))
		sum_squares += price * price
		summand += price
	variance = (sum_squares - (summand * the_mean))/(days - 1)
	return variance
	
def variance_10_day(tick,d):
	return variance(tick,d,10.0)

def variance_30_day(tick,d):
	return variance(tick,d,30.0)


'''Technical functions'''

def covariance(tickA, tickB, d, days=10.0):
	end = datetime.date.today()
	summand = 0.0
	meanA = mean(tickA, d, days)
	meanB = mean(tickB, d, days)
	for i in xrange(1,int(days) + 1):
		day = end - datetime.timedelta(i)
		priceA = float(get_price_expr(tickA, day))
		priceB = float(get_price_expr(tickB, day))
		summand += (priceA - meanA)*(priceB - meanB)
	return (1/(days - 1))*summand	

def covariance_10_days(tickA, tickB, d):
	return covariance(tickA, tickB, d, 10.0)
	
def covariance_30_days(tickA, tickB, d):
	return covariance(tickA, tickB, d, 30.0)

	
	
def correlation(tickA, tickB, d, days=10.0):
	#correlation is simply covariance deflated by its standard deviations
	return covariance(tickA, tickB, d, days)/(std_dev(tickA, d, days)*std_dev(tickB,d,days))

def correlation_10_day(tickA, tickB, d):
	return correlation(tickA, tickB, d, 10.0)

def correlation_30_day(tickA, tickB, d):
	return correlation(tickA, tickB, d, 30.0)


		
		


	
	

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
		'get_short_ratio':'REALTIME',
		'correlation_10_day':'REALTIME',
		'correlation_30_day':'REALTIME',
		'covariance_10_day':'REALTIME',
		'covariance_30_day':'REALTIME',
		'std_dev_10_day':'REALTIME',
		'std_dev_30_day':'REALTIME',
		'mean_10_day':'REALTIME',
		'mean_30_day':'REALTIME',
		'variance_10_day':'REALTIME',
		'variance_30_day':'REALTIME',
	}
