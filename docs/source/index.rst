.. smpl documentation master file, created by
   sphinx-quickstart on Tue Nov 17 13:55:14 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
=================================
|project| |version| documentation
=================================



.. include:: ../../README.md
   :parser: myst_parser.sphinx_


.. toctree::
   :glob:
   :hidden:
   :caption: Links:
   :maxdepth: 3

   GitHub <https://github.com/APN-Pucky/smpl>
 

.. toctree::
   :glob:
   :maxdepth: 3  
   :caption: Examples:

   example/*


:mod:`smpl` package
===================
.. autosummary::
   :toctree: _autosummary
   :template: custom-module-template.rst
   :recursive:
   :caption: Modules:

   smpl
   smpl_io
   smpl_debug
   smpl_doc
   smpl_util
   smpl_io

.. toctree::
   :glob:
   :maxdepth: 3  
   :caption: Profiling:

   performance/*


.. toctree::
   :glob:
   :hidden:
   :caption: Versions:
   :maxdepth: 3

   RTD <https://smpl.readthedocs.io/en/stable/>
   Stable <https://apn-pucky.github.io/smpl/>
   Dev <https://apn-pucky.github.io/smpl/test/>




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
