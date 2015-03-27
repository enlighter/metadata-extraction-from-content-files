#! sudo -E pip install epubzilla

from epubzilla.epubzilla import Epub
import dataterms

def get_epub_info(filename):

	epub = Epub.from_file(filename)
	for element in epub.metadata:
		print "%s : %s" %(element.tag.localname, element.tag.text)
		for k,v in element.tag.iteritems():
			print "\t %s : %s" %(k,v)

	for item in epub.manifest:
		if item.tag.attributes['id'] == dataterms.toc_ncx_id:
			print "got ncx"
			print type(item.get_file())

'''print( get_epub_info("sample.epub") )'''
get_epub_info("sample.epub")