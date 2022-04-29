import os
import sys
from setuptools import setup, find_packages
#import get_suite

DESCRIPTION = "The_system: base system application for ZeroBit"
VERSION = '1.0.0'
LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.rst').read()
except:
    pass

requirements = [
    'django==3.2.13',
    'numpy==1.22.3',
    'pandas==1.4.2',
    'palettable==3.3.0',
    'djangorestframework==3.13.1',
    'django-money==2.1.1',
    'xhtml2pdf==0.2.7',

]

# python setup.py publish
if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    sys.exit()

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Framework :: Django',
]

# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/

setup(
    name='the_system',
    version=VERSION,
    packages=find_packages(exclude=("tests", "tests.*")),
    include_package_data=True,
    author='ZeroBit',
    author_email='support@ZeroBit.tech',
    url='http://github.com/vintasoftware/django-templated-email/',
    license='MIT',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/x-rst',
    platforms=['any'],
    classifiers=CLASSIFIERS,
    install_requires=requirements,
    python_requires = '>=3.8',
    # test_suite = load_tests.get_suite
)
