from setuptools import setup, find_packages

setup(
    name="borg",
    url="https://github.com/esteinig/beastling",
    author="Eike Steinig, Wytamma Wirth",
    author_email="eike.steinig@unimelb.edu.au",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "rich",
        "colorama",
        "pyyaml",
        "black",
        "pytest",
        "requests",
        "pyjwt",
        "typer"
    ],
    entry_points="""
    [console_scripts]
    beastling=beastling.terminal.app
    """,
    version="0.1.0",
    license="MIT",
    description="Beastling is a wrapper for BEAST XMLs that enables configuration of phyldynamic models in Python",
)
