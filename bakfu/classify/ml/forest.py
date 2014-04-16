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
    '''ForestMl
    '''
    init_kwargs = ('n_estimators', )
    #max_depth
    init_method = RandomForestClassifier.__init__
    run_method = RandomForestClassifier.fit_transform

    def __init__(self, *args, **kwargs):
        super(ForestMl, self).__init__(*args, **kwargs)

        n_estimators = kwargs.get('n_estimators', 10)

        self.classifier = RandomForestClassifier(n_estimators=10)
        self._data['classifier'] = self.classifier


    def clusterize(self, data_source, *args, **kwargs):
        '''

        '''

        #>>> X = [[0, 0], [1, 1]]
        #>>> Y = [0, 1]
        #>>> clf = RandomForestClassifier(n_estimators=10)
        #>>> clf = clf.fit(X, Y)

        #self.result = {'clusters':result}
        self.data['result'] = 42

        return result

    def run(self, caller, *args, **kwargs):
        super(ForestMl, self).run(*args, **kwargs)

        data_source = caller.data['main_data']
        #vectorizer_result = caller.data['vectorizer_result']
        vectorizer_result = self.get('vectorizer_result')

        X = StandardScaler(with_mean=False).fit_transform(vectorizer_result)
        db = self.clusterizer.fit(X)

        caller.data['clusterizer_result'] = db

        return self.update(
            result=db,
            clusterizer_result=db)



