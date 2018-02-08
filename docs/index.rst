jellyfish |release|
===================

Overview
--------

jellyfish is a library of functions for approximate and phonetic matching of strings.

Source code is `available on GitHub
<https://github.com/jamesturk/jellyfish>`_

The library provides implementations of the following algorithms:

.. toctree::
   :maxdepth: 3

   phonetic
   stemming
   comparison
   changelog

Implementation
--------------

Each algorithm has C and Python implementations.

On a typical CPython install the C implementation will be used. The Python versions
are available for PyPy and systems where compiling the CPython extension is not
possible.

To explicitly use a specific implementation, refer to the appropriate module::

  import jellyfish._jellyfish as pyjellyfish
  import jellyfish.cjellyfish as cjellyfish

If you've already imported jellyfish and are not sure what implementation you
are using, you can check by querying ``jellyfish.library``::

  if jellyfish.library == 'Python':
      # Python implementation
  elif jellyfish.library == 'C':
      # C implementation


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
