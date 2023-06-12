from setuptools import find_packages, setup

with open("requirements.txt", "r") as requirements_file:
    requirements = requirements_file.read().split("\n")

setup(
    name="pyJudilibre",
    version="0.0.0",
    description="Python Judilibre Client",
    author="Paul Déchorgnat",
    author_email="paul.dechorgnat+pyjudilibre@gmail.com",
    url="https://github.com/pauldechorgnat/pyJudilibre",
    install_requires=requirements,
    packages=find_packages("."),
    licence="MIT",
    include_package_data=True,
    package_data={"": ["*.json"]},
    long_description="",
)
