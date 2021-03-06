# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
import smpl
import re
from sphinx_math_dollar import NODE_BLACKLIST

version = re.sub('^', '', os.popen('git describe --tags').read().strip())


# -- Project information -----------------------------------------------------

project = 'smpl'
copyright = '2020, APN-Pucky'
author = 'APN-Pucky'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [ 'sphinx.ext.autodoc', 'nbsphinx', 'sphinx.ext.githubpages',
    'sphinx.ext.viewcode', 'sphinx.ext.mathjax', 'sphinx.ext.todo', 'sphinx.ext.doctest',
    'matplotlib.sphinxext.plot_directive', 'numpydoc', 'sphinx_math_dollar', 'sphinx.ext.autosummary',
]
#nbsphinx_execute = 'always'
autosummary_generate=True
autosummary_imported_members=True

from docutils.nodes import FixedTextElement, literal,math
from docutils.nodes import  comment, doctest_block, image, literal_block, math_block, paragraph, pending, raw, rubric, substitution_definition, target
math_dollar_node_blacklist = (literal,math,doctest_block, image, literal_block,  math_block,  pending,  raw,rubric, substitution_definition,target) #(FixedTextElement,math)
#print(NODE_BLACKLIST)

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']