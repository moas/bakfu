# -*- coding: utf-8 -*-
from .routes import get_processor


class Chain(object):
    '''
    I guess I shouldn't call this a dragon but ...
    This class can be used to manage data : loading, tagging, classifying...
    '''
    def __init__(self, *args, **kwargs):
        self.data_sources = []
        self.chain = []
        self.base_data = None
        self.data = {}

    def process(self, processor_name, *args, **kwargs):
        '''Process data.'''
        processor = self.run_processor(processor_name, *args, **kwargs)
        self.chain.append(processor)
        return self

    def load(self, processor_name, *args, **kwargs):
        '''Load data.'''

        processor = self.run_processor(processor_name, *args, **kwargs)
        self.data_sources.append(processor)
        self.chain.append(processor)
        if self.base_data == None:
            self.base_data = processor
            self.data['base_data'] = processor
            self.data['main_data'] = processor
        return self

    def run_processor(self, processor_name, *args, **kwargs):
        '''
        TODO?  :
         parse args/kwargs and replace values by variables from local context :
            kwargs['this':'{self.that().this}']→ eval the term
        '''
        processor_class = get_processor(processor_name)

        try:
            previous = self.chain[-1]
        except:
            previous = self

        processor = processor_class.init_run(self, previous, *args, **kwargs)
        processor._prev = previous
        previous._next = processor

        return processor

    def get(self, key):
        '''Returns an item from self.data.''' 
        return self.data[key]

    def get_chain(self, key):
        '''Looks for an item starting at the end of the chain.''' 
        return self.chain[-1].get(key)

    def last(self):
        '''return last element.'''
        return self.chain[-1]

    def __repr__(self):
       chain_str = u' → '.join([str(elt) for elt in self.chain])
       return u'Chain : \n{chain}'.format(chain=chain_str)

__all__ = ['Chain',
           'get_processor',
           ]


'''
exec(open("../README").read())

import nltk.corpus

stopwords= nltk.corpus.stopwords.words('french')

from bakfu.core import Chain
kd = Chain()
data=((0,'Test'),(1,'Autre test'))
kd.load('data.simple',data)
kd.load('data.rest',url="http://0.0.0.0:20001/fortunes/list",key="text")

kd.process('vectorize.sklearn')

kd=Chain().load('data.simple',data_tuples)
.process('vectorize.sklearn',ngram_range=(1,5))
.data


def tokenizer(x):
    def isok(f):
        if len(f)<4:return False
        if f in stopwords:return False
        return True
    x=x.replace("."," ")    
    features = x.split(' ')
    features = [f for f in features if isok(f)]
    return features

#Chain().load('data.simple',data)
.process('vectorize.sklearn',_init={'ngram_range':(2,5)}).data

data=data_tuples
D=Chain().load('data.simple',data)    \
    .process('vectorize.sklearn',    \
    _init=((),{
        'ngram_range':(1,3),
        'min_df':2,
        'max_features':50,
        'stop_words':stopwords,
        'tokenizer':tokenizer,
        }),\
    _run=((),{}))
    
D.data['vectorizer'].get_feature_names()

D.process('cluster.ward')
D.process('cluster.spectral')

Chain()
.load('data.simple',data_tuples)
.process('vectorize.sklearn',ngram_range=(1,5)).data

D=Chain().load('data.redis',_init=((),{'keyname':'data1_3'}))


krom
pip install pytest-cov
py.test --cov bakfu
coverage run --source bakfu -m py.test   ?
coverage report
py.test --cov bakfu test --cov-report=html 


pycme : python classification made easy
dame













exec(open("../README").read())
from bakfu.core import Chain
import nltk.corpus
stopwords= nltk.corpus.stopwords.words('french')
from bakfu.core import Chain
kd=Chain().load('data.simple',data_tuples)
.process('vectorize.sklearn',ngram_range=(1,5)).process('cluster.ward')


kd.process('cluster.ward')


kd=bakfu.Chain()
kd.load('data.xml.ms',file="/home/plloret/OldSeminars/2014/2014-02-florette/export (11).xml",title='Fluide',targets=True)



D.process('cluster.spectral')




'''
