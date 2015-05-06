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
#!/usr/bin/python3

import sys
#import os
from ebooklib import epub  # for epub
# from lxml import etree #for xml, html fast parser
from pprintpp import pprint  # pretty-print
from bs4 import BeautifulSoup as bs  # for html
# try:
# 	import cPickle as pickle
# except:
# 	import pickle
# from dependencies.semanticpy.semanticpy.vector_space import VectorSpace as vs
import utils.dataterms as dataterms
from utils.datahandler import data_dump


class metadata_extraction(epub.EpubReader):
	def __init__(self, filename=''):
		print("Creating new instance")
		epub.EpubReader.__init__(self, filename)
		self.book = self.load()
		self.process()
		self.__reset__()

	def __reset__(self):
		self.def_met = {}
		''' the default metadata from epub's metadata '''
		dc = dataterms.dc_elems()
		self.extracted_elements = dc.dublin_core_elements
		self.manifest = self.container.find('{%s}%s' % (epub.NAMESPACES['OPF'], 'manifest'))
		self._credits_href = ''
		self.html_soup = None
		self.extractor = False # binary flag

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

	def _find_by_(self, description, token_list, section):
		self.extractor = False
		ret = ()
		for token in token_list:
			for header in dataterms.headers[section]:
				if header in token:
					self.extractor = False

			if self.extractor:
				ret += (token,)

			if description in token:
				self.extractor = True
			else:
				try:
					for synonym in dataterms.synonymous[description]:
						if synonym in token:
							self.extractor = True
				except KeyError:
					print("no synonym, continuing...")
		return ret

	def _finishing_touches_(self):
		if self.extracted_elements['creator'] not in self.extracted_elements['contributor']['author']:
			self.extracted_elements['contributor']['author'] += self.extracted_elements['creator']
		# if element_dict['creator'] not in element_dict['contributor']['author']:
		# 	element_dict['contributor']['author'] += element_dict['creator']
		self.extracted_elements.__delitem__('creator')

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

	

	def _get_toc_(self):
		toc = ''
		# get table of contents
		#pprint(self.book.toc)

		def _get_components_(given_list=[]):
			#pprint(given_list)
			components = []
			for item in given_list:
				if item:
					# item is not empty
					#pprint(item)
					if type(item) == tuple:
						item = list(item)
					#print(item)
					if type(item) == list:
						components.extend(_get_components_(item))
					if isinstance(item, epub.Section):
						components.extend([item])
					elif isinstance(item, epub.Link):
						components.extend([item])
			return components

		link_list = _get_components_(self.book.toc)

		for link in link_list:
			if not link:
				# no table of contents present in the book
				print("Table of Contents not found! Continuing...")
				return False
			if link.title:
				if 'credits' in link.title.lower():
					# found credits page:
					if link.href:
						self._credits_href = link.href
						print('%s:%s'%(link.title, link.href))
				if not toc:
					toc += link.title
				else:
					toc += ' -- ' + link.title
		self.extracted_elements['description']['toc'] += (toc,)
		#print(toc)
		# add toc : done
		return True

	def _parse_credits_(self):
		cred = self.book.get_item_with_href(self._credits_href)
		if cred:
			# ack is an epub.EpubHtml type object
			contents = cred.get_content().decode()
			contents = contents[contents.find('<html'):]
			self.html_soup = bs( contents, "lxml")
			#pprint(self.html_soup)
			credits_data = []
			for link in self.html_soup.find_all('p'):
				link_text = link.get_text()
				link_text_stripped = link_text.strip() # strip whitespaces from both ends of the string
				credits_data.extend([link_text_stripped.lower()])
			pprint(credits_data)

			for key in self.extracted_elements['contributor']:
				self.extracted_elements['contributor'][key] += self._find_by_(key, credits_data, '1')
			self.extracted_elements['publisher'] += self._find_by_('publisher', credits_data, '1')
			self.extracted_elements['creator'] += self._find_by_('creator', credits_data, '1')
		else:
			print("Unable to open the credits page!Continuing...")

	def extract_metadata_from_book(self):
		if not self.extracted_elements['description']['toc']:
			self._get_toc_()
		if self._credits_href:
			self._parse_credits_()

	def extract(self):
		self.default_metadata()
		pprint(self.def_met)

		self.extract_default_metadata()
		self.extract_metadata_from_book()
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
	met.save_to_file(met.extracted_elements)
	print(met.manifest)


# get_epub_info("extras/sample0.epub")
get_epub_info("extras/sample1.epub")
#pprint(list(("aby","get")))