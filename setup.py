from codecs import open  # To use a consistent encoding
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='markdown-spring-shell-documentation',
    packages=find_packages(),
    version='1.0.0',
    description='A markdown extension that creates a documentation from Java classes using Spring Shell or https://github.com/fonimus/ssh-shell-spring-boot',
    long_description=long_description,
    author='Dylan Roger',
    author_email='dyl.roger@gmail.com',
    url='https://github.com/dylan-roger/markdown-spring-shell-documentation',
    keywords=['Markdown', 'ssh', 'plugin', 'shell', 'extension'],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=['markdown', 'javalang']
)
