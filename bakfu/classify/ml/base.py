# -*- coding: utf-8 -*-
'''
Base class for machine supervised classifiers.
'''

from abc import abstractmethod
from ...core.classes import Processor

class BaseMl(Processor):
    '''Base class for vectorizers. 
    '''
    def __init__(self, *args, **kwargs):
        super(BaseMl, self).__init__(*args, **kwargs)
        self.clusterizer = None

    def __getattr__(self,attr):
        '''Propagate attribute search to the clusterizer.'''
        try:
            return getattr(self, attr)
        except:
            return getattr(self.clusterizer, attr)

