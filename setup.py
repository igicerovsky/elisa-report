""" Setup for ELISA report module 
"""

from setuptools import setup, find_packages
from elisa_report import VERSION, NAME, DESCRIPTION, LONG_DESCRIPTION

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name=NAME,
    version=VERSION,
    author="Igor Cerovsky",
    author_email="<igor.cerovsky@takeda.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package.

    keywords=['python', 'hamilton', 'report'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Analysts",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
