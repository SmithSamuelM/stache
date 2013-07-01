#!/usr/bin/env python

import sys
import os
from distutils.core import setup

if sys.version_info < (2,5):
    raise NotImplementedError("Sorry, you need at least Python 2.5 to use stace.")

import stache

setup(name='stache',
      version=stache.__version__,
      description='Compact implementation of Mustache logic-less templating. Fork of Stache.',
      long_description=stache.__doc__,
      author=stache.__author__,
      author_email='smith.samuel.m@gmail.com',
      url='https://github.com/SmithSamuelM/stache',
      py_modules=['stache'],
      scripts=['stache.py'],
      license=stache.__license__,
      platforms = 'any',
     )
