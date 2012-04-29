'''
Created on Apr 14, 2012

@author: Paavan
'''
from Demo.backend import Expression

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
    Figure out what function object best fits the string and return a new
    instance of it
    """
    @staticmethod
    def getFunction(func):
        if func.lower() == "stockquote":
            return SimpleFunction(func.lower(), Function.DOLLARS)
        elif func.lower() == "expr_test_a":
            return DummyFunction(func.lower(), Function.NO_UNITS)
        elif func.lower() == "expr_test_b":
            return DummyFunction(func.lower(), Function.NO_UNITS)
    
"""A simple function which only has a stock name parameter"""
class SimpleFunction(Function):
    def __init__(self, func, units):
        super(SimpleFunction, self).__init__(func, units);
        
        self._stock = ""
    
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
    
"""A function that takes date and stock parameters"""
class DateFunction(SimpleFunction):
    def __init__(self, func, units):
        super(DateFunction, self).__init__(func, units);
        
        self.date = "";