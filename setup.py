from setuptools import setup

setup(
    name='ams-recruiting-4',
    version='0.1.0',
    packages=['app', 'app.tests'],
    author='Christoph Raab',
    description='Log Parser to parse a log and find top 10 hosts and http status code stats for first 7 days of july'
)
