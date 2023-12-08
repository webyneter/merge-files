"""Sphinx configuration."""
project = "Merge Files"
author = "Nikita Shupeyko"
copyright = "2023, Nikita Shupeyko"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
