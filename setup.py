from setuptools import setup, find_packages
from epp_gr import __version__

setup(
    name='epp_gr',
    version=__version__ ,
    packages=find_packages(),
    url='https://github.com/martinikola/epp_gr.git',
    license='GPL',
    author='Nektarios',
    author_email='nektarios.arakas@gmail.com',
    description='Epp client for greek registrar',
    install_requires=[
        'beautifulsoup4',
        'bs4',
        'certifi',
        'charset-normalizer',
        'idna',
        'requests',
        'soupsieve',
        'urllib3',
        'python-decouple'
         ],
)
