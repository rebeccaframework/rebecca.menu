from setuptools import setup, find_packages
import os

version = '0.1'

requires = [
    "setuptools>=0.7",
    "pyramid",
]

tests_require = [
    "pytest",
    "testfixtures",
    "rebecca.testing",
]

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='rebecca.menu',
      version=version,
      description="",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "License :: OSI Approved :: MIT License",
        "Framework :: Pyramid",
        ],
      keywords='',
      author='Atsushi Odagiri',
      author_email='aodagx@gmail.com',
      url='https://github.com/rebeccaframework/rebecca.menu',
      license='MIT',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['rebecca'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=tests_require,
      extras_require={
          "testing": tests_require,
      },
)
