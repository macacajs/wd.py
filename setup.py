from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wd',

    version='0.1.9',

    description='Macaca Python Client',
    long_description=long_description,

    url='https://github.com/macacajs/wd.py',

    author='Zichen Zhu',
    author_email='zic.zhu@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords=[
        'macaca',
        'webdriver',
        'uitest',
        'mobile automation',
        'e2e'
    ],

    packages=find_packages(exclude=['tests*', 'docs']),

    install_requires=[
        'enum34',
        'requests',
        'retrying'
    ],

    extras_require={
        'test': ['pytest', 'tox', 'pytest-xdist', 'pytest-cov', 'coverage', 'responses']
    }
)
