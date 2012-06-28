'''
Created on Apr 14, 2012

@author: Paavan
'''
from exprfuncs import *
from backend import Expression, TechnicalExpression

class Function(object):
    NO_UNITS=0
    DOLLARS=1
    PERCENT=2
    """
    Init a function with the string representation of the function we want to call in exprfuncs.py
    For units, use enums defined above
    """
    def __init__(self, func, units):
        self.func = func;
        self.values = [];
        self.units = units
        
    def getUnits(self):
        return self.units;
    
    """
    Subclasses will implement so caller can know whether
    this function is valid in O(1) time
    """
    def isValid(self):
        pass
    
    def setValid(self, valid):
        pass

    """
    Figure out what function object best fits the string and return a new
    instance of it
    """
    @staticmethod
    def getFunction(func):
        if func.lower() == "get_price_expr":
            return SimpleFunction(func.lower(), Function.DOLLARS)
        elif func.lower() == "get_change":
            return SimpleFunction(func.lower(), Function.PERCENT)
        elif func.lower() == "get_volume":
            return SimpleFunction(func.lower(), Function.NO_UNITS)
        elif func.lower() == "get_avg_daily_volume":
            return SimpleFunction(func.lower(), Function.NO_UNITS)
        elif func.lower() == "get_market_cap":  
            return SimpleFunction(func.lower(), Function.DOLLARS)
        elif func.lower() == "get_book_value":
            return SimpleFunction(func.lower(), Function.DOLLARS)
        elif func.lower() == "get_ebitda":
            return SimpleFunction(func.lower(), Function.DOLLARS)
        elif func.lower() == "get_dividend_per_share":
            return SimpleFunction(func.lower(), Function.DOLLARS)
        elif func.lower() == "get_dividend_yield":
            return SimpleFunction(func.lower(), Function.NO_UNITS)
        elif func.lower() == "get_earnings_per_share":
            return SimpleFunction(func.lower(), Function.DOLLARS)
        elif func.lower() == "get_52_week_high":
            return SimpleFunction(func.lower(), Function.DOLLARS)
        elif func.lower() == "get_52_week_low":
            return SimpleFunction(func.lower(), Function.DOLLARS)
        elif func.lower() == "get_50day_moving_avg":
            return SimpleFunction(func.lower(), Function.DOLLARS)
        elif func.lower() == "get_200day_moving_avg":
            return SimpleFunction(func.lower(), Function.DOLLARS)
        elif func.lower() == "get_price_earnings_ratio":
            return SimpleFunction(func.lower(), Function.NO_UNITS)
        elif func.lower() == "get_price_earnings_growth_ratio":
            return SimpleFunction(func.lower(), Function.NO_UNITS)
        elif func.lower() == "get_price_sales_ratio":
            return SimpleFunction(func.lower(), Function.NO_UNITS)
        elif func.lower() == "get_price_book_ratio":
            return SimpleFunction(func.lower(), Function.NO_UNITS)
        elif func.lower() == "get_short_ratio":
            return SimpleFunction(func.lower(), Function.NO_UNITS)
        elif func.lower() == "correlation_10_day":
            return TechnicalFunction(func.lower(), Function.NO_UNITS)
        elif func.lower() == "correlation_30_day":
            return TechnicalFunction(func.lower(), Function.NO_UNITS)
        elif func.lower() == "covariance_10_day":
            return TechnicalFunction(func.lower(), Function.DOLLARS)
        elif func.lower() == "covariance_30_day":
            return TechnicalFunction(func.lower(), Function.DOLLARS)
        elif func.lower() == "mean_10_day":
            return SimpleFunction(func.lower(), Function.DOLLARS)
        elif func.lower() == "mean_30_day":
            return SimpleFunction(func.lower(), Function.DOLLARS)
        elif func.lower() == "std_dev_10_day":
            return SimpleFunction(func.lower(), Function.DOLLARS)
        elif func.lower() == "std_dev_30_day":
            return SimpleFunction(func.lower(), Function.DOLLARS)
        elif func.lower() == "variance_10_day":
            return SimpleFunction(func.lower(), Function.DOLLARS)
        elif func.lower() == "variance_30_day":
            return SimpleFunction(func.lower(), Function.DOLLARS)
        else:
            print 'Error with function definition'
        
    """
    Inflate a function object from an expression object
    """
    @staticmethod
    def inflateFunction(expr):
        #all functions so far are only SimpleFunctions
        func = Function.getFunction(expr.funcName)
        func.setStock(expr.val)
        
        func.setValid(True)
        
        return func
    
"""A technical function contains 2 stock parameters"""
class TechnicalFunction(Function):
    def __init__(self, func, units):
        super(TechnicalFunction, self).__init__(func, units);
        
        self._stockA = ""
        self._stockB = ""
        
        self.validA = False
        self.validB = False

    def isValid(self):
        return (self.validA and self.validB) 
        
    def isAValid(self):
        return self.validA
    
    def setAValid(self, valid):
        self.validA = valid
        
    def isBValid(self):
        return self.validB
    
    def setBValid(self, valid):
        self.validB = valid;
    
    def setStockA(self, stock):
        self._stockA = stock
        
    def setStockB(self, stock):
        self._stockB = stock
    
    def stockA(self):
        return self._stockA; 
    
    def stockB(self):
        return self._stockB
        
    def getExpression(self):
        return TechnicalExpression(self.func, self._stockA, self._stockB)

"""A simple function which only has a stock name parameter"""
class SimpleFunction(Function):
    def __init__(self, func, units):
        super(SimpleFunction, self).__init__(func, units);
        
        self._stock = ""
        
        self.valid = False
        
    def isValid(self):
        return self.valid
    
    def setValid(self, valid):
        self.valid = valid;
    
    def setStock(self, stock):
        self._stock = stock
    
    def stock(self):
        return self._stock;
        
    def getExpression(self):
        return Expression(self.func, self._stock);
    
"""
Dummy function that has a Value parameter
"""
class DummyFunction(Function):
    def __init__(self, func, units):
        super(DummyFunction, self).__init__(func, units);
        
        self.val = ""
    
    def setValue(self, value):
        self.val = value
    
    def value(self):
        return self.val;
        
    def getExpression(self):
        return Expression(self.func, self.val);
    