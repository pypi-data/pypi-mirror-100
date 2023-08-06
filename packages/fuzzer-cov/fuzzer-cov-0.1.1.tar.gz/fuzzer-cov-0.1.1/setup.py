#!/usr/bin/env python3
import os
from setuptools import setup

with open('README.md', 'r') as f:
    readme_content = f.read()
version_string = '0.1.1'

setup(
    name='fuzzer-cov',
    version=version_string,
    long_description=readme_content,
    long_description_content_type='text/markdown',
    entry_points = {
        'console_scripts': [
            'fcov=fuzzer_cov.commands:fuzzer_cov_main'
        ],
    },
    url='https://github.com/Myriad-Dreamin/fuzzer-cov',
    download_url=f'https://github.com/Myriad-Dreamin/fuzzer-cov/archive/v{version_string}.tar.gz',
    author='Myriad Dreamin',
    author_email='camiyoru@gmail.com',
    license='MIT',
    packages=['fuzzer-cov'],
    install_requires=[],
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ]
)