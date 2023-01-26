from setuptools import setup, find_packages
from m2r import parse_from_file
from os import path
from pythern import about

readme_file = path.join(path.dirname(path.abspath(__file__)), 'README.md')
readme = parse_from_file(readme_file)

packages = find_packages()

setup(
    name=about.project,
    version=about.release,
    description=about.description,
    long_description=readme,
    author=about.author,
    author_email=about.author_email,
    url=about.url,
    license=about.license,
    keywords=about.keywords,
    classifiers=about.classifiers,
    packages=packages,
)