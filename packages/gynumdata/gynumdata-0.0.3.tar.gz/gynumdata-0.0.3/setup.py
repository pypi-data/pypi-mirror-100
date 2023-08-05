import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gynumdata",
    version="0.0.3",
    author="Yaw Brother",
    author_email="gsolomonsa@gmail.com",
    description="A simple package calculating values for a single number and created in my Udemy course",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yawbrother/python-pkgdev",
    keywords='package numbers calculations',
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
	    "Operating System :: OS Independent"
    ],
)
