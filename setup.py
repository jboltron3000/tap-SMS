#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-SMS",
    version="0.1.0",
    description="Singer.io tap for extracting data",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_SMS"],
    install_requires=[
        "singer-python>=2.6.0",
        "requests",
    ],
    entry_points="""
    [console_scripts]
    tap-SMS=tap_SMS:main
    """,
    packages=["tap_SMS"],
    package_data = {
        "schemas": ["tap_SMS/schemas/*.json"]
    },
    include_package_data=True,
)
