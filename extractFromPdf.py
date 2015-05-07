''' Run the following command from your shell before running this python code file
    sudo [-E] pip install --upgrade --ignore-installed pdfminer==20140328 or higher version
    
    __author__: "Sushovan Mandal"
    __license__: "GPLv2"
    __email__: "mandal.sushovan92@gmail.com"
'''

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed

# Open a PDF file.
fp = open('extras/sample.pdf', 'rb')
# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)
# Create a PDF document object that stores the document structure.
# Supply the password for initialization.
document = PDFDocument(parser)
# Check if the document allows text extraction. If not, abort.
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed
#parser.set_document(doc)
#doc.set_parser(parser)
#document.initialize()

print(document.info) # The "Info" metadata
#print document.catalog
