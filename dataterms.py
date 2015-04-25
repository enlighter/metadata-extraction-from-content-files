# This module contains the datastructures for metadata extraction

dublin_core_elements = {'title':(),
             'creator': (), # creator to be merged into author in final xml
             'subject':(),
             'description':(), # 2 different subfileds 'abstract' and 'toc' to be created from this field
             'publisher':(),
             'contributor': {
             				'author' : (),
             				'illustrator' : (),
             				'editor' : ()
             				},
             'date': {
             			'created' : (),
             			'accessioned' : (),
             			'copyright' : ()
             			},
             'type':(),
             'format': {
             			'extent' : (),
             			'mimetype' : ()
             			},
             'identifier': {
             				'uri' : (),
             				'isbn' : (),
             				'issn' : (),
             				'citation' : ()
             				},
             'source':(),
             'language':(),
             'relation':(), # 'ispartof', 'ispartofseries', 'haspart', 'isrefencedby', 'refernces' to be got from this
             'coverage':(),
             'rights':()
}

toc_ncx_id = 'ncxtoc'
toc_html_id = 'toc'