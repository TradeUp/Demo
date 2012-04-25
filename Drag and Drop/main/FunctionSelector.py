import Function
import PySide
import sys
from PySide import QtCore
from PySide import QtGui

class FunctionListWidget(QtGui.QListWidget):
	def __init__(self, parent):
		super(FunctionSelector, self).__init__(parent);

"""
ListWidgetItem that is capable of storing the function that it represents
"""
class FunctionListWidgetItem(QtGui.QListWidgetItem):
	def __init__(self, text, parent, func):
		super(FunctionListWidgetItem, self).__init__(text, parent)

		self.func = func