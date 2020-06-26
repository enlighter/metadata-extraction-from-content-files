# metadata-extraction-from-content-files
Extract metadata automatically from educative content files (ebooks, articles, etc.)

Currently supports filetype:
- pdf
- epub

# This repository contains submodules:
To get the complete repository alongwith submodule, clone recursively, i.e.,
- git clone --recursive https://github.com/enlighter/metadata-extraction-from-content-files.git

# Some informtation about functionality:
- extractFromEpub implements endeavour to auto-extract metadata from Epub files like Author, publish date, publish company and many more, which may be relevant for indexing content in a digital library. Such information can be explicitly in the metadata section of directory structure zipped within Epub files. If such explicit metadata is not present, then it tries to extract some metadata information from the first few pages of the content of the book.
- After extracting whatever metadata it can, it indexes the files in SIP format(a specific protocol of directory structure) using the metadata.
- extractor script takes in a folder location from user, finds the epub files within the directory and auto-extracts metadata from them and indexes them into the desired SIP format directory structure.
