import zipfile
from lxml import etree
import dataterms

def get_epub_info(fname):
    ns = {
        'n':'urn:oasis:names:tc:opendocument:xmlns:container',
        'pkg':'http://www.idpf.org/2007/opf',
        'dc':'http://purl.org/dc/elements/1.1/',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'dcterms': 'http://purl.org/dc/terms/'
    }

    # prepare to read from the .epub file
    zip = zipfile.ZipFile(fname)

    # find the contents metafile
    txt = zip.read('META-INF/container.xml')
    #print(txt)
    tree = etree.fromstring(txt)
    cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path',namespaces=ns)[0]
    print(cfname)

    # grab the metadata block from the contents metafile
    cf = zip.read(cfname)
    tree = etree.fromstring(cf)
    print( etree.tostring(tree, pretty_print=True) )
    metadataPath = tree.xpath('/pkg:package/pkg:metadata',namespaces=ns)[0]
    print(metadataPath)
    manifestPath = tree.xpath('/pkg:package/pkg:manifest',namespaces=ns)[0]
    print( len(manifestPath) )

    # repackage the data
    res = {}
    for s in dataterms.DataTerms:
        #check if the element exists before extracting 1st element from the list
        qualifierPath = metadataPath.xpath('dc:%s/text()'%(s),namespaces=ns)
        if len(qualifierPath):  #check if 
            print(qualifierPath)
            res[s] = qualifierPath[0]

    print( metadataPath.xpath('pkg:item',namespaces=ns) )

    return res

print(get_epub_info("sample.epub"))