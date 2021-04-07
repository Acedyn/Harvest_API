import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='harvest_api',
    version='0.1.1',
    author = "Simon Lambin",
    author_email = "slambin@artfx.fr",
    description = ("A REST api to get statistics about CGI projects"),
    packages=find_packages(),
    install_requires=[
          'flask',
          'flask_cors',
          'sqlalchemy',
          'waitress',
          'psycopg2',
          'apscheduler'
    ],
    long_description=read('README.md'),
    include_package_data=True,
)
