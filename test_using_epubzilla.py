#! sudo -E pip install epubzilla

from epubzilla.epubzilla import Epub

def get_epub_info(filename):

	epub = Epub.from_file(filename)
	for element in epub.metadata:
		print "%s : %s" %(element.tag.localname, element.tag.text)
		for k,v in element.tag.iteritems():
			print "\t %s : %s" %(k,v)

'''print( get_epub_info("sample.epub") )'''
get_epub_info("sample.epub")