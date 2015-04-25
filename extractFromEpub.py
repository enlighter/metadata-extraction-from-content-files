''' sudo -E pip install epubzilla
	sudo -E pip install -U epubzilla (upgrade epubzilla and dependencies if already installed)
	[In Ubuntu Systems make sure you have python-dev packages installed in your system ,such as 
	python-dev, python-all-dev, python2.7-dev et al]

	__author__: "Sushovan Mandal"
	__license__: "GPLv2"
	__email__: "mandal.sushovan92@gmail.com"

	use epubzilla=0.1.1
'''

#from epubzilla.epubzilla import Files
#from epubzilla.epubzilla import Epub
from dependencies.epubzilla.epubzilla.epubzilla import Epub, Toc
from lxml import etree
import dataterms

def get_epub_info(filename):

	epub = Epub.from_file(filename)
	#print(epub.metadata.dublin_core_elements)
	metadata = epub.metadata
	for localname in metadata.dublin_core_elements:
		print("%s : %s")%(localname, metadata.get(localname))
		#for key, value in element.attributes.iteritems():
		#	print("\t %s : %s")%(key, value)

	print(epub.author)
	print(epub.container.path_to_content)
	print(epub.manifest[0])
	print(epub.cover)

	for item in epub.manifest:
		if item.attributes['id'] == dataterms.toc_ncx_id:
			print("got ncx")
			print(item.attributes['href'])
			toc_ncx = item.archive
			print(toc_ncx)
			toc_tree = etree.fromstring(toc_ncx)
			print(toc_tree)
			break

'''print( get_epub_info("sample.epub") )'''
get_epub_info("extras/sample.epub")