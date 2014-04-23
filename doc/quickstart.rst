
.. _quickstart:

=================
Quick start
=================

To load a few sentences, vectorize them and clusterize them


.. doctest:: 

    >>> import bakfu
    >>> data = [(i,a) for i,a in enumerate((
    ...            'Test',
    ...            'Other test',
    ...            'Something else',
    ...            'Nevermind'
    ...            ))]
    >>> baf = bakfu.Chain().load('data.simple',data)
    >>> baf.process('vectorize.sklearn')
    >>> baf.process('cluster.ward',n_clusters=2)
    >>> baf.get_chain('result').tolist()
    [0, 0, 1, 0]


Custom processor
=====================

You can write a custom processor and package it with your app. 
You just need to register it.::
    from ..core.routes import register
    from bakfu.data.base import BaseDataSource


    @register('data.mydata')
    class MyData(BaseDataSource):
        def __init__(self, *args, **kwargs):
            super(BaseDataSource, self).__init__(*args, **kwargs)
            self.data = ((0,'this'), (1,'that'))

    from bakfu import Chain
    baf=Chain.load('data.mydata')




