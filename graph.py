'''
Created on Mar 23, 2012

@author: WillIV
'''
import sys
import platform

__version__ = '0.4.1'


import matplotlib

linedict = {}
unusedColors = ['b', 'g', 'r','c','m','y','k']

usedColors = []

#{ name_of_recipe: [(a,b)...], other_recipe: [(a,b)...]} <-- where a*b is the thing you want to graph

'''
this is called by eval in the controller class
send in data in this form:
  {name_of_recipe: ([tuples of values],[dates]), ...}
  '''
def makenew(data,callback,table):
    print 'cheese'
    color = ''
    if(len(unusedColors) >= 1):
        color = unusedColors[0]
        usedColors.append(unusedColors[0])
        del unusedColors[0]
    else:
        color = usedColors[0]
        unusedColors = usedColors[1:]
        usedColors = usedColors[:1]
    
    for n in data:
        linedict.update({n:(data[n][1],(data[n][0][0][0] * data[n][0][0][1]),color)})

    callback(table) # calls the update method on the table 

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
        
#removeline
    
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