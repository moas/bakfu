#!/usr/bin/env python

from distutils.core import setup
from setuptools import  find_packages

setup(name='bakfu',
      version='0.01',
      description='A toolkit for scikit-learn (a toolkit for scipy (a toolkit for python)). Toolkit for clustering, machine learning, natural language processing ...',
      author='Patrick Lloret',
      author_email='plloret@gmx.com',
      url='https://github.com/prmths128/bakfu',
      packages=find_packages(),
      install_requires=[
        'scikit-learn'
        ],
     )
