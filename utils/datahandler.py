import sys
from pprintpp import pprint  # pretty-print
try:
	import cPickle as pickle
except:
	import pickle

class data_dump:
	def __init__(self, to_dump, data_type='extract'):
		self.to_dump = to_dump
		self.type = data_type
		self.__data_dump = None
		self.__data_load = None

	def dump(self):
		try:
			self.__data_dump = open(r'./tmp/%s'%self.type,'wb')
		except:
			e = sys.exc_info()
			pprint(e)
		pickle.dump( self.to_dump, self.__data_dump, -1)
		self.__data_dump.close()

	def load(self):
		try:
			self.__data_load = open(r'./tmp/%s'%self.type,'rb')
		except:
			e = sys.exc_info()
			pprint(e)
		ret = pickle.load(self.__data_load)
		self.__data_load.close()

		return ret