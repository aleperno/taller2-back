#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='backend-test',
      version='0.1',
      description='Test de backend',
      author='Alejandro Pernin',
      author_email='apernin@fi.uba.ar',
      packages=find_packages(exclude=('tests', 'tests.*')),
      )
