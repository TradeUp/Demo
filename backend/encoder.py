# Encoder
#
###

class Encoder:
	"""
	encodes the front-end object as json to be saved into a file """

	def __init__(self,dest):
		self.file = open(dest)
	def save(obj):
		obj.save(self.file)


class Encodeable:
	"""
	an object that is Encodeable
	"""

	def __init__(self):
		self.