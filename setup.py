import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "PyWeibo",
    version = "0.0.1",
    author = "OdinLin",
    author_email = "heyflypig@gmail.com",
    description = ("a tool to crawl and visualize data from Sina Weibo."),
    license = "BSD",
    keywords = "crawler visualization weibo memes",
    url = "https://github.com/sharismlab/Pyweibo",
    packages = find_packages('python'),
    package_dir = {'':'lib'},
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=[
        'setuptools',
        'greenlet',
    ],
    include_package_data=True,
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt']
    }
)