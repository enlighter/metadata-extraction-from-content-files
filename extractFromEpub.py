import zipfile
from lxml import etree
import dataterms

def get_epub_info(fname):
    ns = {
        'n':'urn:oasis:names:tc:opendocument:xmlns:container',
        'pkg':'http://www.idpf.org/2007/opf',
        'dc':'http://purl.org/dc/elements/1.1/'
    }

    # prepare to read from the .epub file
    zip = zipfile.ZipFile(fname)

    # find the contents metafile
    txt = zip.read('META-INF/container.xml')
    print txt
    tree = etree.fromstring(txt)
    cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path',namespaces=ns)[0]
    #print cfname

    # grab the metadata block from the contents metafile
    cf = zip.read(cfname)
    tree = etree.fromstring(cf)
    #print tree
    p = tree.xpath('/pkg:package/pkg:metadata',namespaces=ns)[0]
    #print p

    # repackage the data
    res = {}
    for s in dataterms.DataTerms:
        #check if the element exists before extracting 1st element from the list
        Xpath = p.xpath('dc:%s/text()'%(s),namespaces=ns)
        if Xpath:
            print Xpath
            res[s] = Xpath[0]

    return res

print get_epub_info("sample.epub")