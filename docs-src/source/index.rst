.. sara-spec documentation master file, created by
   sphinx-quickstart on Mon Jun  7 13:58:56 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to sara-spec documentation!
========================================

These tools have been built to handle the reduction of spectroscopic data obtained with the SARA telescope.

There is one module (sara-spec.py) that needs to be in the PYTHONPATH.

Then there is a set of numbered jupyter notebooks (in the notebook folder) that needs to be adjusted for a specific observing night. These notebook also serve as a reduction procedure record.

For the advanced user, it is possible to modify the sara-spec functions for a given dataset -- simply copy over the function you need to modify into the notebook and execute.



.. toctree::
   notebooks/01-Calibrations
   :maxdepth: 1
   :caption: Notebooks:


.. toctree::
   API
   :maxdepth: 1
   :caption: API documentation:

TODO list:
===========

.. todolist::


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
