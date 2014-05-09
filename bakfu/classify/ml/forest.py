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
action : if not specified, a new classifier will be created 
    and used on available data
    if 'fit' : classifier is created but not used
    if 'predict': previous classifier is used
Usage : 
#create clusters
baf.process('cluster.ward')
#load new data
baf.load('data.simple',(...))
#train classifier and use 
baf.process('ml.forest')

TODO: Allow reuse of classifiers.
    '''
    init_kwargs = ('n_estimators', 'classifier', 'data', 'action')
    run_kwargs = ()
    #max_depth
    init_method = RandomForestClassifier.__init__
    run_method = RandomForestClassifier.fit_transform

    def __init__(self, *args, **kwargs):
        super(ForestMl, self).__init__(*args, **kwargs)
        self.action = kwargs.get('action',None)

        if self.action != "predict":
            n_estimators = kwargs.get('n_estimators', 10)
            self.classifier = RandomForestClassifier(n_estimators=n_estimators)
            self._data['classifier'] = self.classifier
        else:
            self.classifier = None

    def _get_classifier(self):
        if self.classifier:
            return self.classifier
        else:
            classifier = self.get('classifier')
            self.classifier = classifier
            return classifier

    def fit(self, caller, *args, **kwargs):
        '''Train a classifier from tagged data'''
        classifier = self._get_classifier()

        vectorizer_result = caller.get('vectorizer_result')
        clusters = caller.get("clusterizer_result")
        classifier.fit(vectorizer_result.toarray(), clusters)

        return classifier

    def predict(self, caller, *args, **kwargs):
        '''Use classifier on new data'''
        classifier = self._get_classifier()
        vectorizer = caller.get_chain('vectorizer')

        #New data
        data_source = caller.get_chain("data_source")
        new_vectorizer_result = vectorizer.transform(data_source.get_data())

        result = self.classifier.predict(new_vectorizer_result.toarray())
        return result

    def run(self, caller, *args, **kwargs):
        super(ForestMl, self).run(caller,*args, **kwargs)

        if self.action in (None, 'fit'):
            result = self.fit(caller, *args, **kwargs)
            self.update(
                result = result,
                classifier = result
                )

        if self.action in (None, 'predict'):
            result = self.predict(caller, *args, **kwargs)
            self.update(
                result=result,
                classifier_result=result
                )

        return self



