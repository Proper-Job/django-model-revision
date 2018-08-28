from setuptools import setup, find_packages

install_requires = [
    'django>1.10.1,<1.11',
]

# Documentation dependencies
documentation_extras = [
    'Sphinx==1.4.9',
]

# Testing dependencies
testing_extras = []

setup(
    name='django-model-revision',
    version='0.0.8',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A Django app.',
    url='https://github.com/Proper-Job/django-model-revision',
    long_description=open('README.rst').read(),
    author='Moritz Pfeiffer',
    author_email='moritz.pfeiffer@alp-phone.ch',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
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
