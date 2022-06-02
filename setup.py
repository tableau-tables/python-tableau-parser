from os import path
from setuptools import setup


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

repo = 'https://github.com/pragdave/mdx_tableau/'
setup(
    name='mdx_tableau',
    version='1.0.0',
    description='Extended table definitions for Markdown',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Dave Thomas (@pragdave)',
    author_email='dave@pragdave.me',
    url=repo,
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation tools',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3'
    ],
    keywords=["markup", "markdown", "table", "rowspan", "colspan", "multimd"],
    install_requires=['Markdown>=3.0'],
    dependency_links=[ 
        'http://github.com/sanscore/py-string-scanner/tarball/master#egg=stringscanner-0.0.2'
    ],
    project_urls={
        'Bug Reports': repo + 'issues',
        'Source': repo
    },
    packages=['mdx_tableau']
)
