import sys
import platform

__version__ = '0.4.1'


import matplotlib



#{ name_of_recipe: [(a,b)...], other_recipe: [(a,b)...]} <-- where a*b is the thing you want to graph

'''
this is called by eval in the controller class
send in data in this form:
  {name_of_recipe: ([tuples of values],[dates]), ...}
  '''
def makenew(Parent, data):    
    Parent.OOps(data)
#    for n in data:
#        Parent.linedict.update({n:(data[n][1],(data[n][0][0][0] * data[n][0][0][1]),color)})

'''assume the dates and money will be sorted already'''        
#def makeLine(name, dates, money, color):
#    print 'hi'
#    linedict.update({name:(dates,money,color)})
#
#'''you will only be adding a point in after the current data points'''
#def addPoint(name, date, money):
#    try:
#        linedict[name][0].append(date)
#        linedict[name][1].append(money)
#    except KeyError:
#        print name + " was not found!"
        
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