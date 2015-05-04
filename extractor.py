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
		self._xml_element_tail = ')'
		self.xml = ''

	def _xml_bind_(self, body=''):
		ret = self._xml_wrapper_head
		if body:
			ret += body
		ret += self._xml_wrapper_tail
		return ret

	def _append_element_(args=''):
		self.xml += self._xml_element_head + args + self._xml_element_tail

	def create_xml(self):
		#self._xml_wrapper = self._xml_wrapper + self._xml_element + '))'
		#print(self._xml_wrapper_head + self._xml_wrapper_tail)
		self.xml = eval(self._xml_bind_())
		# use decode explicitly in python 3 as tostring return a byte type object
		# which needs to be decoded to string (preferably immediately) so the program
		# internally works only on strings
		return tostring( self.xml, xml_declaration=True, encoding='UTF-8').decode()


mt = metadata()
XML = mt.create_xml()
print(XML)