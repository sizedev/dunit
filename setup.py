import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dunit",
    version="0.0.1",
    author="Natalie Fearnley",
    author_email="nfearnley@gmail.com",
    description="Decimal based unit conversion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nfearnley/dunit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)
