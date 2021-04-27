import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="sentida",
    version="2.0.0",
    description="a Danish sentiment library inspired by Vader",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jacob Aarup Dalsgaard, Gustav Aarup Lauridsen, Lars Kjartan Bacher Svendsen and Kenneth Enevoldsen",
    url="https://github.com/Guscode/Sentida2",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data = {"sentida":['emoji_utf8_lexicon.txt', 'sentidav2_lemmas.csv'],},
    # external packages as dependencies
    install_requires=["spacy", "pandas"],
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="NLP danish",
)
