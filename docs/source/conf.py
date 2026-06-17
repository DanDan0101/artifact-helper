# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "artifact-helper"
copyright = "2026, Daniel Sun"
author = "Daniel Sun"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "autoapi.extension",
    "sphinx.ext.mathjax",
    "sphinx_tabs.tabs",
]

autoapi_dirs = ["../../artifact_helper"]
autoapi_add_toctree_entry = False

napoleon_use_param = False
napoleon_use_ivar = True

templates_path = ["_templates"]
# exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinxdoc"
html_static_path = ["_static"]
