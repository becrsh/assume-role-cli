import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="assume-role",
    author="Gerry Put",
    author_email="gerry@theblackcat.company",
    description="A utility to assume aws roles",
    version="0.2.0",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/becrsh/assume-role-cli",
    install_requires=['boto3', 'Click'],
    py_modules=['assume_role'],
    packages=find_packages(),
    include_package_data=True,
    entry_points='''
        [console_scripts]
        assume-role=assume_role.commands:cli
    '''
)
