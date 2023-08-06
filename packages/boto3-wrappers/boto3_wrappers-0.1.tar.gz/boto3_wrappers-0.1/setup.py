from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='boto3_wrappers',
    long_description="Helpful wrappers for boto3.",
    long_description_content_type="text/markdown",
    install_requires=requirements,
    author='Nathan Lichtenstein',
    author_email='nathan@lctnstn.com',
    version='0.1',
    description='Wrapper classes for boto3.',
    packages=find_packages(exclude=('tests', 'docs')),
)
