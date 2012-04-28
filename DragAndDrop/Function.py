'''
Created on Apr 14, 2012

@author: Paavan
'''
from Demo.exprfuncs import *
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
    
"""A simple function which only has a stock name parameter"""
class SimpleFunction(Function):
    def __init__(self, func, units):
        super(SimpleFunction, self).__init__(func, units);
        
        self.stock = ""
    
    def setStock(self, stock):
        self.stock = stock
    
    def stock(self):
        return self.stock;
        
    def getExpression(self):
        return Expression(self.func, self.stock);
    
"""A function that takes date and stock parameters"""
class DateFunction(SimpleFunction):
    def __init__(self, func, units):
        super(DateFunction, self).__init__(func, units);
        
        self.date = "";