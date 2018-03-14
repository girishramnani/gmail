import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as version_file:
    version = version_file.read().strip()

setup(
    name = "gmail",
    version = version,
    author = "https://github.com/girishramnani",
    author_email = "girishramnani95@gmail.com",
    description = ("A Pythonic interface for Google Mail."),
    license = "MIT",
    keywords = "google gmail",
    url = "https://github.com/girishramnani/gmail",
    packages=['gmail'],
    long_description=read('README.txt'),
    install_requires=['pytest'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Communications :: Email",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "rogramming Language :: Python :: 2.7",

    ],
)
