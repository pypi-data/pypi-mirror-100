from setuptools import setup
from setuptools import find_packages
import os
import re

HERE = os.path.abspath(os.path.dirname(__file__))

# store version in the init.py
with open(os.path.join(HERE, "src", "metadata_parser", "__init__.py")) as v_file:
    VERSION = re.compile(r'.*__VERSION__ = "(.*?)"', re.S).match(v_file.read()).group(1)

long_description = (
    description
) = "A module to parse metadata out of urls and html documents"
with open(os.path.join(HERE, "README.rst")) as fp:
    long_description = fp.read()

requires = (
    [
        "BeautifulSoup4",
        "requests>=2.19.1",
        "requests-toolbelt>=0.8.0",
        "six",
    ],
)
tests_require = [
    "httpbin",
    "pytest",
    "pytest-httpbin",
    "responses",
    "tldextract",
]
testing_extras = tests_require + []

# go
setup(
    name="metadata_parser",
    version=VERSION,
    description=description,
    long_description=long_description,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="opengraph protocol facebook",
    author="Jonathan Vanasco",
    author_email="jonathan@findmeon.com",
    url="https://github.com/jvanasco/metadata_parser",
    license="MIT",
    test_suite="tests",
    packages=find_packages(
        where="src",
    ),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=tests_require,
    extras_require={
        "testing": testing_extras,
    },
    entry_points="""
      # -*- Entry points: -*-
      """,
)
