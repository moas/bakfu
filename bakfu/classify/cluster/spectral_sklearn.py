# -*- coding: utf-8 -*-

'''
This is an interface to sklearn vectorizer classes.

'''

from sklearn.cluster import SpectralClustering
from sklearn import metrics
from sklearn.preprocessing import StandardScaler

from ...core.routes import register
from .base import BaseClusterizer


@register('cluster.spectral')
class SpectralClusterizer(BaseClusterizer):
    
    init_kwargs = ('n_clusters',)

    def __init__(self, *args, **kwargs):
        super(SpectralClusterizer, self).__init__(*args, **kwargs)

        self.clusterizer = SpectralClustering(**kwargs)

    def clusterize(self, data_source, *args, **kwargs):   
        '''

        '''

        self.results = {'clusters':result}

        return result

    def run(self, caller, *args, **kwargs):
        data_source = caller.data['main_data']
        vectorizer_result = caller.data['vectorizer_result']

        X = vectorizer_result
        predictions = self.clusterizer.fit_predict(X.toarray())

        caller.data['clusterizer_result'] = predictions
        caller.data['clusterizer'] = self.clusterizer

        return self.update(
            result=predictions,
            clusterizer_result=predictions)

