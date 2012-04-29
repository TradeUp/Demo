import Function, sys
from PySide import QtCore
from PySide import QtGui

class FunctionScrollWidget(QtGui.QScrollArea):
	def __init__(self):
		super(FunctionScrollWidget, self).__init__();

		root = QtGui.QWidget()
		
		layout = QtGui.QVBoxLayout()
		
		layout.addWidget(FunctionItem("Price", "stockquote", self))
		
		layout.addWidget(FunctionItem("Dummy Func Multiply", "expr_test_b", self))
		layout.addWidget(FunctionItem("Dummy Func Divide", "expr_test_a", self))
		
		root.setLayout(layout)
		
		self.setAcceptDrops(True)
		self.setWidget(root)
		
		
	

"""
ListWidgetItem that is capable of storing the function that it represents
"""
class FunctionItem(QtGui.QLabel):
	def __init__(self, text, func, parent):
		super(FunctionItem, self).__init__(text, parent)

		self.func = func

	"""
	Begin dragging this widget
	"""
	def mouseMoveEvent(self, e):
		print "DRAGGING"
		#drag only on left click
		if e.buttons() is not QtCore.Qt.LeftButton: return

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