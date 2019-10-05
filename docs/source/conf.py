# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = 'flaskerize'
copyright = '2019, AJ Pryor, Ph.D.'
author = 'AJ Pryor, Ph.D.'

# -- Documentation configuration ---------------------------------------------
master_doc = 'index'
extensions = [
    'readthedocs_ext.readthedocs',
]

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    
    'display_version': True,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': -1,
    'includehidden': True,
    'titles_only': False
}
