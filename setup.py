#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = "0.1.0"

setup(
    name="radon_kubernetes_metrics",
    version=VERSION,
    description="A module to extract metrics from Terraform scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Michele Moccia",
    maintainer="Michele Moccia",
    author_email="michele.moccia03@gmail.com",
    url="https://github.com/Mikmocc00/radon-terraform-metrics",
    download_url=f"https://github.com/Mikmocc00/radon-kubernetes-metrics/archive/{VERSION}.tar.gz",
    packages=find_packages(exclude=("tests",)),
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
    ],
    
    install_requires=[
        "pyyaml==6.0.2"
    ]
)
