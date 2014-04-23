# -*- coding: utf-8 -*-
'''

'''

import string
import sklearn

from ...core.routes import register
from bakfu.process.base import BaseProcessor

DELIMITER = "<eol>"
DELIMITER_NL = "\n"+DELIMITER+"\n"

try:
    import treetaggerwrapper
except:
    pass

@register('tagging.treetagger')
class TreeTagger(BaseProcessor):
    '''
    Pre-processes data with treetagger.

    :Example:

    >>>from bakfu.examples.dataset1 import DATA
    >>>import nltk
    >>>baf = bakfu.Chain(lang="en")
    >>>baf.load("data.simple",DATA)
    >>>baf.process('tagging.treetagger')
    >>>baf.process('vectorize.sklearn',
    ...        min_df = 2, 
    ...        ngram_range=(1, 3), 
    ...        #stop_words=nltk.corpus.stopwords.words(baf.get('language')),
    ...        max_features=100,
    ...        tokenizer=lambda x:x,
    ...        )
    ...        preprocessor=lambda x:x,
    >>>print(baf.get_chain("vectorizer").get_feature_names())
    >>>print(baf.get_chain("vectorizer_result").toarray()[0])
    '''

    init_args = ()
    init_kwargs = ()
    run_args = ()
    run_kwargs = ()

    def __init__(self, *args, **kwargs):
        super(TreeTagger, self).__init__(*args, **kwargs)


    def run(self, caller, *args, **kwargs):
        '''
        TODO:CLEAN UP 
        '''
        super(TreeTagger, self).run(caller, *args, **kwargs)
        data_source = caller.get_chain('main_data')
        self.caller=caller

        cur_data = data_source.get_data()

        #run treetagger
        text = string.join(cur_data,DELIMITER_NL)
        tagger = treetaggerwrapper.TreeTagger(TAGLANG=caller.get('lang'),TAGDIR='/home/plloret/dev/ms/treetag/',        TAGINENC='utf-8',TAGOUTENC='utf-8')
        tags = tagger.TagText(text)

        #process treetagger output
        tagged_data = []
        buffer = []
        for tag in tags:
            tag = tag.split("\t")
            if tag[0]==DELIMITER:
                buffer = [ (a,b,c if c!='<unknown>' else a) for a,b,c in buffer]
                tagged_data.append(buffer)
                buffer = []
            else:
                buffer.append(tag)

        result = tagged_data

        caller.data['result'] = result
 
        # Remove data according to filtered tags ;
        FILTER_TAGS = ('SENT', 'KON', 'PUN','DT')
        
        data_clean = [
            filter(
                lambda x:x[1] not in FILTER_TAGS
                ,line) 
            for line in tagged_data]

        data_clean = [
            filter(
                lambda x:len(x[2])>2
                ,line) 
            for line in data_clean]

        #remove tags ; only keep cannonical form
        data_clean = [[ d[2] for d in line] for line in data_clean]

        #reformat data to ((id,data),...)
        #note: data now contains lists of tokens instead of sentences
        uids = data_source.get_uids()
        new_data = zip(uids,data_clean)
        data_source.data = new_data
        data_source.meta_data = {"tokenized":True}

        self._data.update(
            {'result':result,
             'tagger_result':result,
            })

        return self
