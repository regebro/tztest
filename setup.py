from setuptools import setup, find_packages
import sys, os

version = '3.1'

setup(name='tztest',
      version=version,
      description="Cross-platform timezone testinfo.",
      long_description="""\
This package is an attempt of finding a cross-platform way to figure out what time zone you are in.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='timezone',
      author='Lennart Regebro',
      author_email='regebro@gmail.com',
      url='',
      license='Public Domain',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
