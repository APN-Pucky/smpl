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
from docutils.nodes import literal, math
from docutils.nodes import doctest_block, image, literal_block, math_block,  pending, raw, rubric, substitution_definition, target

from ipywidgets.embed import DEFAULT_EMBED_REQUIREJS_URL

import re
import os
import datetime
import sys
sys.path.insert(0, os.path.abspath('../..'))

version = re.sub('^', '', os.popen('git describe --tags').read().strip())


# -- Project information -----------------------------------------------------

project = 'smpl'
copyright = str(datetime.datetime.now().year) + ', APN-Pucky'
author = 'APN-Pucky'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 'nbsphinx', 'sphinx.ext.githubpages',
              'sphinx.ext.viewcode', 'sphinx.ext.mathjax', 'sphinx.ext.todo', 'sphinx.ext.doctest',
              'matplotlib.sphinxext.plot_directive', 'numpydoc', 'sphinx_math_dollar', 'sphinx.ext.autosummary',
              'sphinx.ext.coverage','jupyter_sphinx','jupyter_sphinx.execute'
              ]
#nbsphinx_execute = 'always'
autosummary_generate = True
autosummary_imported_members = True

math_dollar_node_blacklist = (literal, math, doctest_block, image, literal_block,  math_block,
                              pending,  raw, rubric, substitution_definition, target)  # (FixedTextElement,math)
# print(NODE_BLACKLIST)

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
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_js_files = [
    DEFAULT_EMBED_REQUIREJS_URL,
]
html_css_files = [
    "style.css",
]
html_extra_path = ['../prof/combined.svg']