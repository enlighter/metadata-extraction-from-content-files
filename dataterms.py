# This module contains the datastructures for metadata extraction

dublin_core_elements = {'title':(),
             'creator': (), # creator to be merged into author in final xml
             'subject':(),
             'description':(), # 2 different subfileds 'abstract' and 'toc' to be created from this field
             'publisher':(),
             'contributor': {
             				'author' : (),
             				'illustrator' : (),
             				'editor' : (),
                                    'none' : ()
             				},
             'date': {
             			'created' : (),
             			'accessioned' : (),
             			'copyright' : (),
                              'none' : ()
             			},
             'type':(),
             'format': {
             			'extent' : (),
             			'mimetype' : (),
                              'none' : ()
             			},
             'identifier': {
             				'uri' : (),
             				'isbn' : (),
             				'issn' : (),
             				'citation' : (),
                                    'none' : ()
             				},
             'source':(),
             'language':(),
             'relation':(), # 'ispartof', 'ispartofseries', 'haspart', 'isrefencedby', 'refernces' to be got from this
             'coverage':(),
             'rights':()
}

# dc_elements_helper = {
#       'author' :
# }

synonymous = {
      'illustrator' : ("graphics", "cover",)
}

# headers

first = ["author","editor","illustrator","graphics","cover","coordinator","indexer","proofreader","reviewer"]
headers = {
      '1' : first
}

toc_ncx_id = 'ncxtoc'
toc_html_id = 'toc'