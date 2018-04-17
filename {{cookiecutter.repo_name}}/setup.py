import os
import sys
from setuptools import setup, find_packages
import subprocess


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

conda_install = subprocess.call('conda env create -f environment.yml', shell=True)

requires = [
    ]

setup(name='{{cookiecutter.repo_name}}',
      version='1.0',
      description='{{cookiecutter.short_description}}',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',   
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='ecoreleve_server',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = {{cookiecutter.repo_name}}:main
      [console_scripts]
      initialize_{{cookiecutter.repo_name}}_db ={{cookiecutter.repo_name}}.scripts.initializedb:main
      """,
      )
