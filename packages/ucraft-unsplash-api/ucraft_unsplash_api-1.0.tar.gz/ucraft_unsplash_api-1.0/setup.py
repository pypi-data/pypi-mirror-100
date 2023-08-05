#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="ucraft_unsplash_api",
    version="1.0",
    description="A Python client for the Unsplash API.",
    license="MIT",
    author="UC",
    author_email="",
    url="https://github.com/levon2111/unsplash_api.git",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "oauthlib==2.0.1",
        "requests==2.25.1",
        "requests-oauthlib==0.7.0",
        "six==1.15.0",
    ],
    keywords="unsplash api python",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    zip_safe=True,
)
