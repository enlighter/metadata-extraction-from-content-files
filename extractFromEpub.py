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

	for key,value in dataterms.dublin_core_elements.iteritems() :
		if type(value) == dict:
			for k,v in value.iteritems():
				print "%s : %s" %(k, metadata.get(k))
		else:
			print "%s : %s" %(key, metadata.get(key))

	print "author : %s" %(epub.author)

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