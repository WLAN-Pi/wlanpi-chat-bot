# -*- coding: utf-8 -*-

import os
from codecs import open

from setuptools import find_packages, setup

# load the package's __version__.py module as a dictionary
metadata = {}

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "chatbot", "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), metadata)

extras = {
    "development": [
        "black",
        "isort",
        "mypy",
        "flake8",
        "pytest",
    ],
}

# fmt: off
setup(
    name=metadata["__title__"],
    version=metadata["__version__"],
    description=metadata["__description__"],
    long_description=metadata["__description__"],
    author=metadata["__author__"],
    author_email=metadata["__author_email__"],
    url=metadata["__url__"],
    python_requires="~=3.7,",
    license=metadata["__license__"],
    platforms=["linux"],
    packages=find_packages(),
    install_requires=[
        "requests==2.27.1",
        "timeout_decorator==0.5.0",
        "psutil==5.9.0",
        "netifaces==0.11.0",
        "PyYAML==6.0",
        "Pillow==9.0.1",
        "qrcode==7.4",
    ],
    extras_require=extras,
    project_urls={
        "Documentation": "https://docs.wlanpi.com",
        "Source": metadata["__url__"],
    },
    classifiers=[
        "Natural Language :: English",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: System Administrators",
        "Topic :: Utilities",
    ],
    keywords="Chat, Bot, Chatbot",
    include_package_data=True,
    entry_points={"console_scripts": ["chatbot=chatbot.__main__:main"]},
)
