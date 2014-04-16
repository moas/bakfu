# -*- coding: utf-8 -*-

import pytest

from bakfu.core import Chain
from bakfu.classify.cluster import ward_sklearn
from bakfu.data.simple import SimpleDataSource
from bakfu.process.vectorize.vec_sklearn import CountVectorizer
from bakfu.classify.cluster.ward_sklearn import WardClusterizer

def test_cluster():
    
    data=((0,'data test 1'),
          (1,'Data test 2'),
          (2,'other data test 3.')
          )
    test_subject = Chain().load('data.simple',data).process('vectorize.sklearn').process('cluster.ward')

    
    assert isinstance(test_subject.chain[0],SimpleDataSource)
    assert isinstance(test_subject.chain[1],CountVectorizer)
    assert isinstance(test_subject.chain[2],WardClusterizer)
    
    result = test_subject.get_chain('result')
    assert len(result) == len(data)

    assert result.tolist() == test_subject.chain[-1].get('result').tolist()
    assert result.tolist() == test_subject.chain[-1]._data['result'].tolist()


