''' sudo [-E] pip install ebooklib
	[In Ubuntu based systems make sure you have python-dev packages installed in your system,
	such as python-dev, python-all-dev, python3-dev et al]
	sudo [-E] pip install pprintpp
	sudo [-E] pip install beautifulsoup4
	In case of python2 as system default, use pip3 instead

	__author__: "Sushovan Mandal"
	__license__: "GPLv2"
	__email__: "mandal.sushovan92@gmail.com"

	use python >= 3.4
	use ebooklib=0.15
'''
# !/usr/bin/python2

import sys
import os
from ebooklib import epub  # for epub
# from lxml import etree #for xml, html fast parser
from pprintpp import pprint  # pretty-print
from bs4 import BeautifulSoup as bs  # for html

try:
	import cPickle as pickle
except:
	import pickle
# from dependencies.semanticpy.semanticpy.vector_space import VectorSpace as vs
import dataterms

# def get_html_from_manifest(epub, key, value):
# 	for item in epub.manifest:
# 		if item.tag.attributes[key] == value:
# 			print "got %s" %value
# 			return item.get_file()

# def create_soup_from_html_dump():
# 	html_soup = bs( pickle.load(html_dump), "lxml") #markup using lxml's html parser

# 	html_dump.close()
# 	return html_soup

# def find_by(description, token_list, section):
# 	extract = False
# 	ret = ()
# 	for token in token_list:
# 		for header in dataterms.headers[section]:
# 			if header in token:
# 				extract = False

# 		if extract:
# 			ret += (token,)

# 		if description in token:
# 			extract = True
# 		else:
# 			try:
# 				for synonym in dataterms.synonymous[description]:
# 					if synonym in token:
# 						extract = True
# 			except KeyError:
# 				print("no synonym, continuing...")
# 	return ret

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

class metadata_extraction(epub.EpubReader):
	def __init__(self, filename=''):
		print("Creating new instance")
		epub.EpubReader.__init__(self, filename)
		self.book = self.load()
		self.process()
		self.__reset__()
		# self.ee_helper = dataterms.

	def __reset__(self):
		self.def_met = {}
		''' the default metadata from epub's metadata '''
		dc = dataterms.dc_elems()
		self.extracted_elements = dc.dublin_core_elements

	def _reduce_list_(self, given_list=[]):
		''' relevant to ebooklib metadata elements '''
		ret_dict = {}

		for element in given_list:
				''' type(element) = tuple '''
				namespace = epub.NAMESPACES['OPF']
				sub_dict = element[1]
				''' type(sub_dict) = dict '''
				if sub_dict:
					for k,v in sub_dict.items():
						if namespace not in k:
							ret_dict[v] = element[0]
						else :
							ret_dict[element[0]] = None
				else:
					ret_dict[element[0]] = None

		return ret_dict

	def _value_from_(self, get_dict={}):
		''' relevant to dictionaries returned by _reduce_list_ '''
		ret = ()

		for k,v in get_dict.items():
			if v:
				''' if this condition is fulfilled then get_dict element is a
				sub-qualifier value '''
				ret += (v,)
			else:
				''' if this condition is fulfilled then get_dict element is a
				standalone value '''
				ret += (k,)

		return ret

	def _finishing_touches_(self):
		if self.extracted_elements['creator'] not in self.extracted_elements['contributor']['author']:
			self.extracted_elements['contributor']['author'] += self.extracted_elements['creator']
		# if element_dict['creator'] not in element_dict['contributor']['author']:
		# 	element_dict['contributor']['author'] += element_dict['creator']
		self.extracted_elements.__delitem__('creator')

		# ret = dict(element_dict)
		# ret.__delitem__('creator')
		# #del ret['creator']
		# return ret

	def default_metadata(self):
		namespace = epub.NAMESPACES['DC']
		self.def_met = self.book.metadata[namespace]

	def extract_default_metadata(self):
		pprint(self.extracted_elements)

		for key,value in self.def_met.items() :
			''' type(value) = list. '''
			print("%{0}%".format(key))
			pprint(value)
			sub_dict = self._reduce_list_(value)
			pprint(sub_dict)

			if key in self.extracted_elements:
				if type(self.extracted_elements[key]) == dict:
					''' if this condition is fulfilled then check if sub_dict element is a
					standalone value or if it is a sub-qualifier value '''
					for k,v in sub_dict.items():
						if v:
							''' if this condition is fulfilled then sub_dict element is a
							sub-qualifier value '''
							if k in self.extracted_elements[key]:
								self.extracted_elements[key][k] += (v,)
						else:
							''' if this condition is fulfilled then sub_dict element is a
							standalone value '''
							self.extracted_elements[key]['none'] += (k,)
				else:
					self.extracted_elements[key] += self._value_from_(sub_dict)
			else:
				for k in self.extracted_elements:
					if key in self.extracted_elements[k]:
						self.extracted_elements[k][key] += self._value_from_(sub_dict)

	def extract(self):
		self.default_metadata()
		pprint(self.def_met)

		self.extract_default_metadata()
		self._finishing_touches_()

		pprint(self.extracted_elements)

	def save_to_file(self, to_save):
		filer = data_dump(to_save)
		filer.dump()

	def load_from_file(self):
		filer = data_dump(None)
		return filer.load()

	def __str__(self):
		return "Class <metadata_extraction(epub.EpubReader)>"

	def __repr__(self):
		return "metadata_extraction(\"" + self.file_name + "\")"


def get_epub_info(filename):
	book = epub.read_epub(filename)
	# metadata = book.metadata
	# pprint(metadata)
	met = metadata_extraction(filename)
	print(met)
	print(repr(met))
	#met.extract_default_metadata()
	met.extract()


get_epub_info("extras/sample0.epub")
get_epub_info("extras/sample1.epub")