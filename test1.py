'''
Created on Mar 12, 2012

@author: WillIV
'''
#!/usr/bin/python
 
import datetime
import numpy as np
import matplotlib.colors as colors
import matplotlib.finance as finance
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager


stockArray = [[datetime.date(2006,1,1), datetime.date.today(), 'IBM'],[datetime.date(2006,1,1), datetime.date.today(), 'SPY']]

startdate = datetime.date(2006,1,1)
today = enddate = datetime.date.today()
ticker = 'IBM'


fh = finance.fetch_historical_yahoo(ticker, startdate, enddate)
# a numpy record array with fields: date, open, high, low, close, volume, adj_close)

r = mlab.csv2rec(fh); fh.close()
r.sort()
print r

fh2  = finance.fetch_historical_yahoo('AAPL', startdate, enddate)
r2 = mlab.csv2rec(fh2); fh2.close()
r2.sort()

def moving_average(x, n, type='simple'):
    """
    compute an n period moving average.

    type is 'simple' | 'exponential'

    """
    x = np.asarray(x)
    if type=='simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))

    weights /= weights.sum()


    a =  np.convolve(x, weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a

plt.rc('axes', grid=True)
plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)

textsize = 9
left, width = 0.1, 0.8
rect = [left, 0.1, width, 0.8]

fig = plt.figure(facecolor='white')
axescolor  = '#f6f6f6'  # the axies background color


ax2 = fig.add_axes(rect, axisbg=axescolor)

prices = r.adj_close
fillcolor = 'darkgoldenrod'


### plot the price and volume data
dx = r.adj_close - r.close
low = r.low + dx
high = r.high + dx

deltas = np.zeros_like(prices)
deltas[1:] = np.diff(prices)
up = deltas>0
#ax2.vlines(r.date[up], low[up], high[up], color='black', label='_nolegend_')
#ax2.vlines(r.date[~up], low[~up], high[~up], color='black', label='_nolegend_')
ma20 = moving_average(prices, 1, type='simple')
#ma200 = moving_average(prices, 200, type='simple')

linema20, = ax2.plot(r.date, ma20, color='b', lw=2, label='IBM Moving Average (20)')
#linema200, = ax2.plot(r.date, ma200, color='r', lw=2, label='IBM Moving Average (200)')

prices2 = r2.adj_close
dx2 = r2.adj_close - r2.close
low2 = r2.low + dx2
high2 = r2.high + dx2

#deltas2 = np.zeros_like(prices2)
#deltas2[1:] = np.diff(prices2)
#up2 = deltas2>0
#ax2.vlines(r.date[up], low[up], high[up], color='black', label='_nolegend_')
#ax2.vlines(r.date[~up], low[~up], high[~up], color='black', label='_nolegend_')
ma220 = moving_average(prices2, 20, type='simple')
ma2200 = moving_average(prices2, 200, type='simple')

linema220, = ax2.plot(r2.date, ma220, color='g', lw=2, label='AAPL Moving Average (20)')
linema2200, = ax2.plot(r2.date, ma2200, color='m', lw=2, label='AAPL Moving Average (200)')


last = r[-1]
s = '%s O:%1.2f H:%1.2f L:%1.2f C:%1.2f, V:%1.1fM Chg:%+1.2f' % (
    today.strftime('%d-%b-%Y'),
    last.open, last.high,
    last.low, last.close,
    last.volume*1e-6,
    last.close-last.open )
#t4 = ax2.text(0.3, 0.9, s, transform=ax2.transAxes, fontsize=textsize)

props = font_manager.FontProperties(size=10)
leg = ax2.legend(loc='center left', shadow=True, fancybox=True, prop=props)
leg.get_frame().set_alpha(0.5)


# turn off upper axis tick labels, rotate the lower ones, etc
'''for ax in ax2:
    if ax!=ax2:
        for label in ax.get_xticklabels():
            label.set_visible(False)
    else:'''
for label in ax2.get_xticklabels():
    label.set_rotation(30)
    label.set_horizontalalignment('right')

ax2.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')



class MyLocator(mticker.MaxNLocator):
    def __init__(self, *args, **kwargs):
        mticker.MaxNLocator.__init__(self, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return mticker.MaxNLocator.__call__(self, *args, **kwargs)

# at most 5 ticks, pruning the upper and lower so they don't overlap
# with other ticks
#ax2.yaxis.set_major_locator(mticker.MaxNLocator(5, prune='both'))
#ax3.yaxis.set_major_locator(mticker.MaxNLocator(5, prune='both'))

ax2.yaxis.set_major_locator(MyLocator(5, prune='both'))
#ax3.yaxis.set_major_locator(MyLocator(5, prune='both'))

plt.show()
#plt.savefig('graph', format='png')