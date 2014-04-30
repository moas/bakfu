# -*- coding: utf-8 -*-

'''
This is an interface to sklearn vectorizer classes.

'''

import sklearn

from sklearn.feature_extraction.text import CountVectorizer as SKCountVectorizer

from ...core.routes import register
from .base import BaseVectorizer

import nltk.corpus

nltk.corpus.stopwords.words("english")


@register('vectorize.sklearn')
class CountVectorizer(BaseVectorizer):
    '''
    sklearn CountVectorizer
    '''
    init_args = ()
    init_kwargs = ('ngram_range', 'min_df',
                   'max_features', 'stop_words',
                   'tokenizer')
    run_args = ()
    run_kwargs = ()

    def __init__(self, *args, **kwargs):
        super(CountVectorizer, self).__init__(*args, **kwargs)

        self.vectorizer = SKCountVectorizer(*args, **kwargs)

    def vectorize(self, data_source, *args, **kwargs):
        '''
        Calls fit_transform or transform.
        '''
        # If vectorizer has already been use, reuse it for the new data set
        if hasattr(self.vectorizer, 'vocabulary_'):
            result = self.vectorizer.transform(data_source.get_data(),
                                               *args, **kwargs)
        else:
            result = self.vectorizer.fit_transform(data_source.get_data(),
                                                   *args, **kwargs)
        self.results = {'vectorizer':result}
        return result

    def run(self, caller, *args, **kwargs):
        super(CountVectorizer, self).run(caller, *args, **kwargs)
        data_source = caller.get_chain('data_source')

        #obj.run(*args, **kwargs)
        result = self.vectorizer.fit_transform(data_source.get_data())
        self.results = {'vectorizer':self.vectorizer, 'data':result}

        caller.data['vectorizer'] = self.vectorizer
        caller.data['result'] = result
        caller.data['vectorizer_result'] = result

        self.update(
            result=result,
            vectorizer_result=result,
            vectorizer=self.vectorizer
            )

        return self

    @classmethod
    def init_run(cls, caller, *args, **kwargs):
        '''
        By default, args and kwargs are used when creating Vectorizer

        Chain().load('data.simple',data).
          process('vectorize.sklearn',_init={'ngram_range':(2,5)}).data

        Chain().load('data.simple',data)    \
            .process('vectorize.sklearn',    \
            _init=((),{'ngram_range':(2,5)}),\
            _run=((),{}))
        '''
        if '_init' in kwargs or '_run' in kwargs:
            return CountVectorizer.init_run_static(CountVectorizer,
                                                   caller,
                                                   *args, **kwargs)

        obj = cls(*args, **kwargs)
        obj.run(caller)

        return obj
