import Function, sys
from PySide import QtCore
from PySide import QtGui

class FunctionScrollWidget(QtGui.QScrollArea):
	def __init__(self):
		super(FunctionScrollWidget, self).__init__();

		root = QtGui.QWidget()
		
		layout = QtGui.QVBoxLayout()
		
		layout.addWidget(FunctionItem("get_price_expr", self))
		layout.addWidget(FunctionItem("get_change", self))
		layout.addWidget(FunctionItem("get_volume", self))
		layout.addWidget(FunctionItem("get_avg_daily_volume", self))
		layout.addWidget(FunctionItem("get_stock_exchange", self))
		layout.addWidget(FunctionItem("get_market_cap", self))
		layout.addWidget(FunctionItem("get_book_value", self))
		layout.addWidget(FunctionItem("get_ebitda", self))
		layout.addWidget(FunctionItem("get_dividend_per_share", self))
		layout.addWidget(FunctionItem("get_dividend_yield", self))
		layout.addWidget(FunctionItem("get_earnings_per_share", self))
		layout.addWidget(FunctionItem("get_52_week_high", self))
		layout.addWidget(FunctionItem("get_52_week_low", self))
		layout.addWidget(FunctionItem("get_50day_moving_avg", self))
		layout.addWidget(FunctionItem("get_200day_moving_avg", self))
		layout.addWidget(FunctionItem("get_price_earnings_ratio", self))
		layout.addWidget(FunctionItem("get_price_earnings_growth_ratio", self))
		layout.addWidget(FunctionItem("get_price_sales_ratio", self))
		layout.addWidget(FunctionItem("get_price_book_ratio", self))
		layout.addWidget(FunctionItem("get_short_ratio", self))

		
		root.setLayout(layout)
		
		self.setAcceptDrops(True)
		self.setWidget(root)
	
	@staticmethod
	def getDisplayNameForFunction(funcName):
		if funcName == "get_price_expr":
			return "Price"
		elif funcName == "get_change":
			return "Change"
		elif funcName == "get_volume":
			return "Volume"
		elif funcName == "get_avg_daily_volume":
			return "Avg Daily Volume"
		elif funcName == "get_stock_exchange":
			return "Stock Exchange"
		elif funcName == "get_market_cap":
			return "Market Cap"
		elif funcName == "get_book_value":
			return "Book Value"
		elif funcName == "get_ebitda":
			return "EBITDA"
		elif funcName == "get_dividend_per_share":
			return "Dividend/Share"
		elif funcName == "get_dividend_yield":
			return "Dividend Yield"
		elif funcName == "get_earnings_per_share":
			return "Earnings per Share"
		elif funcName == "get_52_week_high":
			return "52 Week High"
		elif funcName == "get_52_week_low":
			return "52 Week Low"
		elif funcName == "get_50day_moving_avg":
			return "50 day moving avg"
		elif funcName == "get_200day_moving_avg":
			return "200 day moving avg"
		elif funcName == "get_price_earnings_ratio":
			return "Price Earnings Ratio"
		elif funcName == "get_price_earnings_growth_ratio":
			return "Price Earnings Growth Ratio"
		elif funcName == "get_price_sales_ratio":
			return "Price Sales Ratio"
		elif funcName == "get_price_book_ratio":
			return "Price Book Ratio"
		elif funcName == "get_short_ratio":
			return "Short Ratio"

	

"""
ListWidgetItem that is capable of storing the function that it represents
"""
class FunctionItem(QtGui.QLabel):
	def __init__(self, func, parent):
		print func
		super(FunctionItem, self).__init__(FunctionScrollWidget.getDisplayNameForFunction(func), parent)

		self.func = func

	"""
	Begin dragging this widget
	"""
	def mouseMoveEvent(self, e):
		#drag only on left click
		if e.buttons() != QtCore.Qt.LeftButton: return

		mimedata = QtCore.QMimeData()
		drag = QtGui.QDrag(self)
		#the MIME data will be text. It will be the text of this item + / + the function to call
		mimedata.setText(self.text() + '/' + self.func)

		#draw the right pixmap
		pixmap = QtGui.QPixmap()
		pixmap = pixmap.grabWidget(self)

		drag.setMimeData(mimedata)
		drag.setPixmap(pixmap)

		drag.start(QtCore.Qt.CopyAction);