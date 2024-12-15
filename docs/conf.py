# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath("../"))

def find_version(filename):
    """
    Find package version in file.
    """
    import re

    content = Path(filename).read_text()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Hyper-DB'
copyright = '2024, Yifan Feng'
author = 'Yifan Feng'
release = find_version("../hyperdb/__init__.py")

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
autodoc_typehints = "none"

# mathjax_path = 'https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",  # 自动提取 type hints
    "sphinx.ext.viewcode",
    "sphinx.ext.doctest",
    "sphinx.ext.mathjax",
    "sphinxcontrib.bibtex",
    "sphinx_copybutton",
]
autosummary_generate = True

# for bibtex config
bibtex_bibfiles = ["refs.bib"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
import sphinx_rtd_theme

html_theme = 'sphinx_rtd_theme'
# html_logo = "_static/logo_DHG_white.svg"
html_theme_options = {
    # "style_nav_header_background": "#9C27B0",
    "logo_only": True,
    "collapse_navigation": False,
}
html_static_path = ['_static']

def setup(app):
    app.add_css_file("css/hyper_db.css")