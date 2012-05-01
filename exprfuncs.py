#
# Expression Functions
##
from matplotlib.finance import quotes_historical_yahoo
import datetime

def expr_test_b(x,d):
	return x*((d%2)+1) # starts with 5 
def expr_test_a(x,d):
	return x # starts with 10

def stockquote(tick,d):
	""" returns the avg price on a given day """
	return quotes_historical_yahoo(tick,d,d)[0][-2] # makes a lot of unsafe assumptions

"""
1. price -- done (stockquote)
2. PE 
3. div yield
4. YTD
5. beta
""" 
