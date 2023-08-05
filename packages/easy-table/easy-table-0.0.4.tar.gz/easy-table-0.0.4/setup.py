import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "easy-table",
    version = "0.0.4",
    author = "iz1kga",
    author_email = "iz1kga@gmail.com",
    description = "easy-table replacement",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "",
    license = "MIT License",
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
    packages = ["easy_table"],
    python_requires = '>=3.6'
)
