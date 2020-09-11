# setup for package TEA (Taxa Evaluation and Assessment)

from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(name="TEA",
        version="0.0.1",
        author="Melissa Gray",
        author_email="mag535@drexel.edu",
        description="A package to parse, organize, calculate, and save data from metagenomic profile files",
        long_description=readme,
        long_description_content_type="text/markdown",
        url="https://github.com/mag535/TEA/",
        packages=find_packages();
        classifiers=[
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approves :: GNU General Public License v3"]
        )
