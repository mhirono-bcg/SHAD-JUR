from setuptools import find_packages, setup

setup(
    name="src",
    version="1.0.0",
    packages=find_packages(),
    author="Hirono, Masatake",
    author_email="masatakehirono1351@gmail.com",
    license="MIT",
    entry_points={"console_scripts": ["generate_jur_ss_outputs=src.core:cli"]},
)
