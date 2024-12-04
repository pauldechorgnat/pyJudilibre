from setuptools import setup, find_packages
from pyjudilibre.__version__ import __version__

with open("requirements.txt", "r", encoding="utf-8") as file:
    requirements = [f.split("/")[-1].split("@")[0] for f in file.read().split("\n")]

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="pyjudilibre",
    version=__version__,
    author="Paul Déchorgnat",
    author_email="paul.dechorgnat@gmail.com",
    url="https://github.com/pauldechorgnat/pyJudilibre",
    packages=find_packages(),  # ["pyjudilibre"],
    description="A small Python wrapper for Judilibre API",
    license="MIT",
    include_package_data=True,
    long_description=long_description,
    data_files=[("config", ["requirements.txt"])],
    long_description_content_type="text/markdown",
    install_requires=requirements,
    classifiers=[
        # How mature is this project? Common values are
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish (see also "license" above)
        # "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
