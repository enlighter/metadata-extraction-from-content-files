''' sudo -E pip install epubzilla
	sudo -E pip install -U epubzilla (upgrade epubzilla and dependencies if already installed)
	[In Ubuntu based systems make sure you have python-dev packages installed in your system,
	such as python-dev, python-all-dev, python2.7-dev et al]

	__author__: "Sushovan Mandal"
	__license__: "GPLv2"
	__email__: "mandal.sushovan92@gmail.com"

	use epubzilla=0.1.1
'''

#from epubzilla.epubzilla import Files
from epubzilla.epubzilla import Epub
from lxml import etree
import dataterms


def get_epub_info(filename):


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

	print extracted_elements

	for item in epub.manifest:
		if item.tag.attributes['id'] == dataterms.toc_html_id:
			print "got toc"
			toc_ncx = item.get_file()
			#print toc_ncx
			#toc_tree = etree.fromstring(toc_ncx)
			#print toc_tree
			break

'''print( get_epub_info("sample.epub") )'''
get_epub_info("extras/sample.epub")