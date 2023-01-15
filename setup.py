# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='weather',
    version='0.1.0',
    description='Dead simple rpi-zero based weather station',
    long_description=readme,
    author='Matteo Brancaleoni',
    author_email='mbrancaleoni@gmail.com',
    url='https://github.com/xadhoom/rpi-weather',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
