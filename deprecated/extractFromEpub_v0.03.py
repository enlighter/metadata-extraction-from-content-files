''' sudo [-E] pip install ebooklib
	[In Ubuntu based systems make sure you have python-dev packages installed in your system,
	such as python-dev, python-all-dev, python2.7-dev et al]
	sudo [-E] pip install pprintpp
	sudo [-E] pip install beautifulsoup4
	In case of python3 as system default, use pip2 instead

	__author__: "Sushovan Mandal"
	__license__: "GPLv2"
	__email__: "mandal.sushovan92@gmail.com"

	use python2.7
	use epubzilla=0.1.1
'''
#!/usr/bin/python2

import sys
import os
from epubzilla.epubzilla import Epub #for epub
#import zipfile
#from lxml import etree #for xml, html fast parser
import lxml
from pprintpp import pprint #pretty-print
from bs4 import BeautifulSoup as bs #for html
try:
   import cPickle as pickle
except:
   import pickle
#from dependencies.semanticpy.semanticpy.vector_space import VectorSpace as vs
import dataterms

def get_html_from_manifest(epub, key, value):
	for item in epub.manifest:
		if item.tag.attributes[key] == value:
			print "got %s" %value
			return item.get_file()

def dump_html(to_dump):
	#os.chdir('tmp')
	#os.listdir(r'./')
	try:
		html_dump = open(r'./tmp/temp_html','wb')
	except:
		e = sys.exc_info()
		pprint(e)
	#os.chdir('..')

	pickle.dump( to_dump, html_dump, -1)
	html_dump.close()

def create_soup_from_html_dump():
	try:
		html_dump = open(r'./tmp/temp_html','rb')
	except:
		e = sys.exc_info()
		pprint(e)
		return

	html_soup = bs( pickle.load(html_dump), "lxml") #markup using lxml's html parser

	html_dump.close()
	return html_soup

def finishing_touches(element_dict):
	if element_dict['creator'] not in element_dict['contributor']['author']:
		element_dict['contributor']['author'] += element_dict['creator']

	ret = dict(element_dict)
	del ret['creator']
	return ret

def find_by(description, token_list, section):
	extract = False
	ret = ()
	for token in token_list:
		for header in dataterms.headers[section]:
			if header in token:
				extract = False

		if extract:
			ret += (token,)

		if description in token:
			extract = True
		else:
			try:
				for synonym in dataterms.synonymous[description]:
					if synonym in token:
						extract = True
			except KeyError:
				print "no synonym, continuing..."
	return ret

def get_epub_info(filename):

	#archive = zipfile.ZipFile(filename)
	epub = Epub.from_file(filename)
	metadata = epub.metadata

	extracted_elements = dataterms.dublin_core_elements
	#print extracted_elements

	for key,value in extracted_elements.iteritems() :
		if type(value) == dict:
			for k,v in value.iteritems():
				text = metadata.get(k)
				if text:
					extracted_elements[key][k] += (text,)
		else:
			text = metadata.get(key)
			if text:
				extracted_elements[key] += (text,)
	 
	if epub.author:
		extracted_elements['contributor']['author'] += (epub.author,)

	#extracted_elements['creator']  += ("testing",)

	# # for item in epub.manifest:
	# # 	if item.tag.attributes['id'] == dataterms.toc_html_id:
	# # 		print "got toc"
	# # 		toc_ncx = item.get_file()
	# # 		#print toc_ncx
	# # 		#toc_tree = etree.fromstring(toc_ncx)
	# # 		#print toc_tree
	# # 		break

	dump_html( get_html_from_manifest(epub, 'id', dataterms.toc_html_id) )

	# HCREDITS : extract 'credits' info from html
	soup = create_soup_from_html_dump()
	for link in soup.find_all('a'):
		link_text = link.get_text().encode('utf8')
		if link_text.lower() == 'credits':
			credits_file = link.get('href')
	# HCREDITS: done

	dump_html( get_html_from_manifest(epub, 'href', credits_file) )

	soup = create_soup_from_html_dump()
	credits_data = []
	for link in soup.find_all('p'):
		#print link.contents
		#link_text = link.string
		link_text = link.get_text().encode('utf8')
		link_text_stripped = link_text.strip() # strip whitespaces from both ends of the string
		credits_data.extend([link_text_stripped.lower()])

		# for debugging :
		pickle.dump( link_text, sys.stdout )
		# pickle the list using highest protocol avalailable
		# that is what -1 signifies
	#print credits_data
	#vector_space = vs(credits_data)
	#print vector_space.related(0)

	# HEXTCREDITS: extract from credits
	pprint(extracted_elements)
	for key in extracted_elements['contributor']:
		extracted_elements['contributor'][key] += find_by(key, credits_data, '1')
	print type(extracted_elements['publisher'])
	extracted_elements['publisher'] += find_by('publisher', credits_data, '1')
	extracted_elements['creator'] += find_by('creator', credits_data, '1')
	# HEXTCREDITS: done

	extracted_elements = finishing_touches(extracted_elements)
	pprint(extracted_elements)

'''print( get_epub_info("sample.epub") )'''
get_epub_info("extras/sample.epub")