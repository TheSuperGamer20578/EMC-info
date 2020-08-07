from setuptools import setup, find_packages

classifiers = [
    'Development Status :: Alpha',
    'Intended Audience :: Gaming',
    'Programming Language :: Python :: 3'
]

setup(
    name='EMC info',
    version='0.0.1',
    description='A package to get info from the minecraft server EarthMC',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='TheSuperGamer20578',
    author_email='emc@thesupergamer20578.ml',
    license='',
    classifiers=classifiers,
    keywords='',
    packages=find_packages(),
    install_requires=['']
)