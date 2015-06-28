# -*- coding: utf-8 -*-

import os
from setuptools import setup

hitcount = __import__('hitcount')

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-hitcount",
    version=hitcount.__version__,
    include_package_data=True,
    packages=['hitcount'],
    url='http://github.com/thornomad/django-hitcount',
    license='BSD',
    description="Hit counting application for Django.",
    long_description=README,
    author='Damon Timm',
    author_email='damontimm@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    zip_safe=False,
)
