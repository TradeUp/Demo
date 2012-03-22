#
# Expression Functions
##
from matplotlib.finance import quotes_historical_yahoo
import datetime

def expr_test_b(x,d):
	return x*d
def expr_test_a(x,d):
	return x/d

def stockquote(tick,d):
	""" returns the avg price on a given day """
	return quotes_historical_yahoo(tick,d,d)[0][-2] # makes a lot of unsafe assumptions
