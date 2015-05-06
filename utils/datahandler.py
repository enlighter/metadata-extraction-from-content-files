import sys
from pprintpp import pprint  # pretty-print
try:
	import cPickle as pickle
except:
	import pickle

class data_dump:
	def __init__(self, to_dump, data_type='extract', dump_path='./tmp/'):
		self.to_dump = to_dump
		self.dump_path = dump_path
		self.type = data_type
		self._data_dump = None
		self._data_load = None
		self._is_binary = True

	def dump(self):
		if self._is_binary:
			try:
				# write mode = binary
				#self._data_dump = open(r'./tmp/%s'%self.type,'wb')
				self._data_dump = open(self.dump_path + self.type,'wb')
			except:
				e = sys.exc_info()
				pprint(e)
			pickle.dump( self.to_dump, self._data_dump, -1)
			self._data_dump.close()
		else:
			# write mode = text
			# Todo: in case of non-binary object the object my change
			# object may even need to be user-defined
			try:
				with open(self.dump_path + self.type,'w') as self._data_dump:
					self._data_dump.write(self.to_dump)
			except:
				e = sys.exc_info()
				pprint(e)

		# self._data_dump.close()

	def load(self):
		try:
			self._data_load = open(r'./tmp/%s'%self.type,'rb')
		except:
			e = sys.exc_info()
			pprint(e)
		ret = pickle.load(self._data_load)
		self._data_load.close()

		return ret

class xml_dump(data_dump):
	''' wrapper class around data_dump class above '''
	def __init__(self, to_dump):
		data_dump.__init__(self, to_dump, 'dublin_core.xml')
		self._is_binary = False

# class html_dump(data_dump):
# 	''' wrapper class around data_dump class above '''
# 	# fo