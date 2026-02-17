lifegraph
=========

**lifegraph** visualises your life as a grid of weekly squares, inspired by
the `Wait But Why <https://waitbutwhy.com/2014/05/life-weeks.html>`_ blog
post.

.. image:: _static/alife.png
   :alt: Example life graph
   :align: center
   :width: 60%

Installation
------------

.. code-block:: bash

   pip install lifegraph

Quick start
-----------

.. code-block:: python

   from lifegraph import Lifegraph
   from datetime import date

   g = Lifegraph(date(1990, 11, 1))
   g.add_title("My Life")
   g.save("my_life.png")

.. toctree::
   :maxdepth: 2
   :caption: Contents

   auto_examples/index
   api
   changelog
   CONTRIBUTING
   CODE_OF_CONDUCT

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
