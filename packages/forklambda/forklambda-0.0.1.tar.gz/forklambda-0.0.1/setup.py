from setuptools import setup

setup(
        name='forklambda',
        version='0.0.1',
        author='Zachary Lefin',
        author_email='zachlefin@gmail.com',
        packages=['forklambda'],
        url='http://pypi.python.org/pypi/forklambda/',
        license='LICENSE',
        description='A lambda function implementation with variable argument ordering.',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown'
        )
