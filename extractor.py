''' [In Ubuntu based systems make sure you have python-dev packages installed in your system,
	such as python-dev, python-all-dev, python3-dev et al]
	sudo [-E] pip install lxml
	sudo [-E] pip install pprintpp
	In case of python2 as system default, use pip3 instead

	__author__: "Sushovan Mandal"
	__license__: "GPLv2"
	__email__: "mandal.sushovan92@gmail.com"

	use python >= 3.4
	use ebooklib=0.15
'''
#!/usr/bin/python3

import sys
import os
from pprintpp import pprint  # pretty-print
from lxml.etree import tostring
from lxml.builder import E
from extractFromEpub import metadata_extraction as epub_extraction
from utils.datahandler import xml_dump, empty_contents

class metadata:
	def __init__(self):
		self._xml_wrapper_head = 'E.dublin_core('
		self._xml_wrapper_tail = ',schema="dc")'
		self._xml_element_head = 'E.dcvalue('
		self._xml_element_tail = ' language="en")'
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
		if self._xml_body:
			self._xml_body += ','
		self._xml_body += self._xml_element_head + args + self._xml_element_tail
		print(self._xml_body)

	def _create_xml_(self):
		self.xml = eval(self._xml_bind_(self._xml_body))
		# use decode explicitly in python 3 as tostring returns a byte type object
		# which needs to be decoded to string (preferably immediately) so the program
		# internally works only on strings
		return tostring( self.xml, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode()

class epub_data(metadata):
	def __init__(self, epub_file):
		metadata.__init__(self)
		self.epub_extractor = epub_extraction(epub_file)

	def execute(self):
		self.epub_extractor.extract()
		return self.create_xml()

	def load(self):
		self.epub_extractor.extracted_elements = dict(self.epub_extractor.load_from_file())

	def write_xml(self, xml_string, sub_directory='100001/'):
		xml_writer = xml_dump(xml_string, sub_directory)
		#print(xml_writer.to_dump)
		xml_writer.dump()

	def create_xml(self):
		for key,value in self.epub_extractor.extracted_elements.items():
			if type(value) == dict:
				for k,v in self.epub_extractor.extracted_elements[key].items():
					if v:
						for element in v:
							attr = '"' + element + '", element="' + key + '", qualifier="' + k + '",'
							#print(attr)
							self._append_element_(attr)
			elif value:
				# value is a tuple here
				for element in value:
					attr = '"' + element + '", element="' + key + '", qualifier="none",'
					#print(attr)
					self._append_element_(attr)

		return self._create_xml_()

class sipData():
	"""docstring for sipData : 
	Creates SIP format directory
	structure with data from required
	metadata classes"""
	def __init__(self, filename, mode=''):
		if 'epub' in mode.lower():
			self.met = epub_data(filename)
		elif 'pdf' in mode.lower():
			self.met = None
			# Todo: pdf_data class to be made
			# and instantiated here
		else:
			return False

		self.filename = filename
		self.contents = None

	def execute(self):
		dc_xml = self.met.execute()
		print(dc_xml)
		sub_path = 100001 # sip sub-directory id
		for i in range(9999):
			full_path = './import/' + str(sub_path) + '/'
			try:
				if os.path.exists(full_path):
					sub_path = sub_path + i
					continue
				else:
					os.makedirs(full_path)
					break
			except:
				e = sys.exc_info()
				pprint(e)
				print("Aborting...")
				return False

		sub_directory = str(sub_path) + '/'
		# write the dublin_core.xml
		self.met.write_xml(dc_xml, sub_directory)
		# write the empty contents file
		self.contents = empty_contents('', sub_directory)
		self.contents.dump()


mySip = sipData("extras/sample1.epub", 'epub')
mySip.execute()