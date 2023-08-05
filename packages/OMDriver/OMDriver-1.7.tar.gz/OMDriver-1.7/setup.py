from distutils.core import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
  name = 'OMDriver',
  packages = ['OMDriver'], # this must be the same as the name above
  version = '1.7',
  description = 'Simplify3x Object Picker Data Retrieval',
  author = 'Simplify3x',
  long_description=long_description,
  long_description_content_type = 'text/markdown',
  author_email = 'simplifyom@simplify3x.com',
  keywords = ['string', 'reverse'],
  url='https://github.com/Simplify3x/OMDriver',
  classifiers = [],
  install_requires=['requests']
)