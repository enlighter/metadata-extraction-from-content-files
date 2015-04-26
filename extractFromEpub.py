''' sudo [-E] pip install epubzilla
	sudo [-E] pip install -U epubzilla (upgrade epubzilla and dependencies if already installed)
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
import zipfile
#from lxml import etree #for xml, html fast parser
from pprintpp import pprint #pretty-print
from bs4 import BeautifulSoup as bs #for html
try:
   import cPickle as pickle
except:
   import pickle
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
					extracted_elements[key][k] = text
		else:
			text = metadata.get(key)
			if text:
				extracted_elements[key] = text
	 
	if epub.author:
		extracted_elements['contributor']['author'] += epub.author

	pprint(extracted_elements)

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
	credits_data = soup.find_all('p')
	for link in credits_data:
		#print link.contents
		#link_text = link.string
		link_text = link.get_text().encode('utf8')
		#print type(link_text)
		link_text_stripped = link_text.strip() # strip whitespaces from both ends of the string

		# for debugging :
		pickle.dump( link_text, sys.stdout )
		# print link_text
		# pickle the list using highest protocol avalailable
		# that is what -1 signifies

'''print( get_epub_info("sample.epub") )'''
get_epub_info("extras/sample.epub")