from setuptools import setup, find_packages

setup(
    name='epp_gr',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/mpizeli/eppgr',
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
