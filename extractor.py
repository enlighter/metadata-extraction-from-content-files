''' [In Ubuntu based systems make sure you have python-dev packages installed in your system,
	such as python-dev, python-all-dev, python3-dev et al]
	sudo [-E] pip install lxml
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
from pprintpp import pprint  # pretty-print
from lxml.etree import tostring
from lxml.builder import E
from extractFromEpub import metadata_extraction as epub_extraction

class metadata:
	def __init__(self):
		self._xml_wrapper_head = 'E.dublin_core("",'
		self._xml_wrapper_tail = 'schema="dc")'
		self._xml_element_head = 'E.dcvalue('
		self._xml_element_tail = 'language="en")'
		self._xml_body = ''
		self.xml = ''

	def _xml_bind_(self, body=''):
		ret = self._xml_wrapper_head
		if body:
			ret += body
		ret += self._xml_wrapper_tail
		print("whole xml structure:")
		print(ret)
		return ret

	def _append_element_(self, args=''):
		self._xml_body += self._xml_element_head + args + self._xml_element_tail
		print(self._xml_body)

	def _create_xml_(self):
		self.xml = eval(self._xml_bind_(self._xml_body))
		# use decode explicitly in python 3 as tostring return a byte type object
		# which needs to be decoded to string (preferably immediately) so the program
		# internally works only on strings
		return tostring( self.xml, xml_declaration=True, encoding='UTF-8').decode()

class epub_data(metadata):
	def __init__(self):
		metadata.__init__(self)
		self.epub_extractor = epub_extraction('extras/sample1.epub')

	def load(self):
		self.epub_extractor.extracted_elements = dict(self.epub_extractor.load_from_file())

	def create_xml(self):
		for key,value in self.epub_extractor.extracted_elements.items():
			if type(value) == dict:
				for k,v in self.epub_extractor.extracted_elements[key].items():
					if v:
						for element in v:
							attr = element + ', element="' + key + '", qualifier="' + k + '",'
							print(attr)
							self._append_element_(attr)
			elif value:
				# value is a tuple here
				for element in value:
					attr = element + ', element="' + key + '", qualifier="none",'
					print(attr)
					self._append_element_(attr)


mt = epub_data()
mt.load()
pprint(mt.epub_extractor.extracted_elements)
XML = mt.create_xml()
print(XML)