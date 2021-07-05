from setuptools import setup, find_packages

setup(
    name="critter",
    url="https://github.com/esteinig/critter",
    author="Eike Steinig, Wytamma Wirth",
    author_email="eike.steinig@unimelb.edu.au",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "rich",
        "fastapi",
        "colorama",
        "pyyaml",
        "black",
        "pytest",
        "pydantic",
        "requests",
        "typer",
        "coverage"
    ],
    entry_points="""
    [console_scripts]
    critter=critter.terminal.app
    """,
    version="0.1.0",
    license="MIT",
    description="Critter enables configuration of phylodynamic models for pathogen transmission dynamics in Python",
)
