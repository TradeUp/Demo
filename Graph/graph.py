'''
Created on Mar 23, 2012

@author: WillIV
'''
import sys
import platform

__version__ = '0.4.1'


import matplotlib

linedict = {}

'''assume the dates and money will be sorted already'''        
def makeLine(name, dates, money, color):
    print 'hi'
    linedict.update({name:(dates,money,color)})

'''you will only be adding a point in after the current data points'''
def addPoint(name, date, money):
    try:
        linedict[name][0].append(date)
        linedict[name][1].append(money)
    except KeyError:
        print name + " was not found!"
        

    
'''
Colors
b    blue
g    green
r    red
c    cyan
m    magenta
y    yellow
k    black
w    white
'''