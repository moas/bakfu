# -*- coding: utf-8 -*-
'''
Random Forest classifier
'''

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler

from ...core.routes import register
from .base import BaseMl
from sklearn.ensemble import RandomForestClassifier

@register('ml.forest')
class ForestMl(BaseMl):
    '''Random forest
Parameters (not implemented yet) : 
classifier : if not specified, create a new classifier.    
data : if not specified, get most recent data from the chain.

Usage : 
#create clusters
baf.process('cluster.ward')
#load new data
baf.load('data.simple',(...))
#train classifier and use 
baf.process('ml.forest')

TODO: Allow reuse of classifiers.
    '''
    init_kwargs = ('n_estimators', 'classifier', 'data')
    run_kwargs = ('action')
    #max_depth
    init_method = RandomForestClassifier.__init__
    run_method = RandomForestClassifier.fit_transform

    def __init__(self, *args, **kwargs):
        super(ForestMl, self).__init__(*args, **kwargs)

        n_estimators = kwargs.get('n_estimators', 10)

        self.classifier = RandomForestClassifier(n_estimators=n_estimators)
        self._data['classifier'] = self.classifier

    def run(self, caller, *args, **kwargs):
        super(ForestMl, self).run(caller,*args, **kwargs)

        vectorizer_result = caller.get_chain('vectorizer_result')
        clusters = caller.get("clusterizer_result")
        vectorizer = caller.get_chain('vectorizer')
        self.classifier.fit(vectorizer_result.toarray(), clusters)

        #New data
        data_source = caller.get_chain("data_source")
        new_vectorizer_result = vectorizer.transform(data_source.get_data())

        result = self.classifier.predict(new_vectorizer_result.toarray())

        return self.update(
            result=result,
            classifier_result=result
            )



