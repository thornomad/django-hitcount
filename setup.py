import os
from setuptools import setup, find_packages
 
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
 
setup(
    name = "django-hitcount",
    version = "0.2",
    url = 'http://github.com/thornomad/django-hitcount',
    license = 'BSD',
    description = "Django hit counter application that tracks the number of hits/views for chosen objects",
    long_description = read('README'),
 
    author = 'Damon Timm',
    author_email = 'damontimm@gmail.com',
 
    packages = find_packages(),
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
