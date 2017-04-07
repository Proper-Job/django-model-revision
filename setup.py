import os

from model_revisions import __version__
from setuptools import setup, find_packages

install_requires = [
    'django>1.10.1<1.11',
]

# Documentation dependencies
documentation_extras = [
    'Sphinx==1.4.9',
]

# Testing dependencies
testing_extras = []

setup(
    name='django-model-revisions',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    license='Proprietary', 
    description='A Django app.',
    long_description=open('README.rst').read(),
    author='Moritz Pfeiffer',
    author_email='moritz.pfeiffer@alp-phone.ch',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: Proprietary',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=install_requires,
    extras_require={
        'docs': documentation_extras,
        'testing': testing_extras,
    },
)
