'''
Created on Apr 14, 2012

@author: Paavan
'''
from ...backend import exprfuncs
from ...backend.backend import Expression

class Function():
    """
    Init a function with the string representation of the function we want to call in exprfuncs.py
    """
    def __init__(self, func):
        self.func;
        pass
    
"""A simple function which only has a stock name parameter"""
class SimpleFunction(Function):
    def __init__(self, func):
        super(SimpleFunction, self).__init__(func);
        
        self.stock = ""
    
    def setStock(self, stock):
        self.stock = stock
        
    def getExpression(self):
        return Expression(self.func, self.stock);
    
"""A function that takes date and stock parameters"""
class DateFunction(SimpleFunction):
    def __init__(self, func):
        super(DateFunction, self).__init__(func);
        
        self.date = "";