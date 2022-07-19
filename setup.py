from setuptools import setup

setup(
    name='google_scrapper',
    version='1.0.0',
    packages=['src'],
    url='https://github.com/EvertonTomalok/google-scrapper',
    license='gpl-3.0',
    author='Everton Tomalok',
    author_email='evertontomalok123@gmail.com.br',
    description='Google Search Ean Scrapper',
    install_requires=[
        'click',
        'random-user-agent==1.0.1',
        'requests-html==0.10.0',
        'nest-asyncio==1.4.3',
        'pymongo==3.11.2',
        'psycopg2==2.8.6',
        'dataclasses-json==0.5.2',
        'schematics==2.1.0',
        'python-dotenv==0.15.0',
    ],
    entry_points='''
        [console_scripts]
        google=src.ports.cli.main:cli
    ''',
)
