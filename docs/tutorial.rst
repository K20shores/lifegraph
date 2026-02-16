Tutorial
========

This tutorial walks through creating a life graph from scratch, adding
events, eras, and customisations along the way.

Creating your first grid
------------------------

The minimal life graph needs only a birthdate.  Every square in the grid
represents one week of your life.

.. code-block:: python

   from lifegraph import Lifegraph
   from lifegraph.configuration import Papersize
   from datetime import date

   birthday = date(1990, 11, 1)
   g = Lifegraph(birthday, dpi=300, size=Papersize.A4,
                  axes_rect=[.1, .1, .8, .8])
   g.save("grid.png")

By default the axes leave room on the sides for annotation labels.  The
``axes_rect`` parameter controls how much of the page the grid occupies --
``[left, bottom, width, height]`` in figure-fraction coordinates.

Adding a title and watermark
----------------------------

.. code-block:: python

   g = Lifegraph(birthday, dpi=300, size=Papersize.A4)
   g.add_title("Time is Not Equal to Money")
   g.add_watermark("Your Life")
   g.save("titled.png")

:meth:`~lifegraph.Lifegraph.add_title` places text above the grid.
:meth:`~lifegraph.Lifegraph.add_watermark` overlays faint diagonal text
across the whole axes.

Changing the age range
----------------------

The grid has 90 rows by default.  You can change the maximum age and
optionally display the number at the bottom of the grid:

.. code-block:: python

   g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)
   g.show_max_age_label()
   g.save("max_age.png")

Showing a sub-range with ``min_age``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can set a minimum age to display only a portion of the grid.  This
is useful when you want to focus on a specific period of life -- for
example, the working years.  Events outside the visible range are stored
but not drawn, eras that cross the boundary are clipped automatically,
and era spans entirely outside the range are skipped.  The y-axis labels
show the actual ages.

.. code-block:: python

   from lifegraph import Lifegraph, Side
   from lifegraph.configuration import Papersize
   from datetime import date

   birthday = date(1990, 11, 1)
   g = Lifegraph(birthday, dpi=300, size=Papersize.A4,
                  max_age=65, min_age=20)

   g.add_title("The Working Years")

   g.add_life_event("First real job", date(2013, 6, 15), color="#00008B")
   g.add_life_event("Got promoted", date(2018, 3, 1),
                     color="#006400", side=Side.LEFT)
   g.add_life_event("Bought a house", date(2021, 9, 10), color="#8B0000")

   g.add_era("Career at Acme", date(2013, 6, 15), date(2025, 1, 1),
             color="#4423fe")
   g.add_era_span("Grad school", date(2012, 9, 1), date(2014, 5, 15),
                   color="#D2691E")

   g.save("working_years.png")

``min_age`` defaults to ``0``, so existing code is unaffected.

Adding life events
------------------

A life event is a labeled point on the grid.  The position is calculated
automatically from the birthdate and the event date.

.. code-block:: python

   from lifegraph import Lifegraph, Side
   from lifegraph.configuration import Papersize
   from datetime import date

   birthday = date(1990, 11, 1)
   g = Lifegraph(birthday, dpi=300, size=Papersize.A4)

   # Random color when none is given
   g.add_life_event("My first paycheck", date(2006, 8, 23))

   # Hex color + force label to the left side
   g.add_life_event("Graduated\nhighschool", date(2008, 6, 2),
                     color="#00FF00", side=Side.LEFT)

   # RGB tuple
   g.add_life_event("First car", date(2010, 7, 14), color=(1, 0, 0))

   g.save("events.png")

Key parameters:

* **color** -- any matplotlib color (hex string, RGB tuple, named color).
  A random color is chosen when omitted.
* **side** -- force the label to :attr:`~lifegraph.Side.LEFT` or
  :attr:`~lifegraph.Side.RIGHT`.
* **hint** -- a ``(x, y)`` coordinate hint for the label position (mutually
  exclusive with *side*).
* **color_square** -- when ``True`` (the default), the grid square itself is
  colored to match the label text.

Adding eras
-----------

Eras shade a rectangular region of the grid behind the squares:

.. code-block:: python

   g.add_era("College", date(2008, 9, 1), date(2012, 5, 15),
             color="blue", alpha=0.2)

The *alpha* parameter (default ``0.3``) controls the shading opacity.

Adding era spans
----------------

Era spans draw a dumbbell shape -- circles at the start and end positions
connected by a line:

.. code-block:: python

   g.add_era_span("Road trip", date(2015, 6, 1), date(2015, 8, 30),
                   color="#D2691E")

Set ``color_start_and_end_markers=True`` to also color the grid squares at
the endpoints.

Overlaying an image
-------------------

You can overlay an image that fills the grid area:

.. code-block:: python

   g.add_image("photo.jpg", alpha=0.5)

The *alpha* parameter controls transparency.

Customising the grid style
--------------------------

Lifegraph ships with a bundled ``.mplstyle`` file that provides the
default appearance (marker shape, spine visibility, tick layout, etc.).
Size-dependent values such as font sizes and marker sizes are computed
automatically from the chosen paper size.

You can override any setting through ``g.settings.rcParams``:

.. code-block:: python

   # Change marker shape and size
   g.settings.rcParams["lines.marker"] = "v"
   g.settings.rcParams["lines.markersize"] = 2.0

   # Move the x-axis label
   g.format_x_axis(positionx=0.5, color="red")

   # Customise the y-axis label
   g.format_y_axis(text="Your Age", color="green")

Advanced users can also use matplotlib's style system directly with the
bundled style path, or combine it with their own style sheets:

.. code-block:: python

   import matplotlib.pyplot as plt
   from lifegraph.configuration import STYLE_PATH

   plt.style.use(STYLE_PATH)          # apply the lifegraph defaults
   plt.style.use([STYLE_PATH, "my_overrides.mplstyle"])  # layer styles

The full set of configurable parameters for each paper size is defined in
:class:`~lifegraph.configuration.LifegraphParams`.  Some parameters can
also be set through convenience methods like
:meth:`~lifegraph.Lifegraph.format_x_axis` and
:meth:`~lifegraph.Lifegraph.format_y_axis`.  For example,
``g.format_x_axis(positionx=0, positiony=0)`` is equivalent to
``g.settings.otherParams['xlabel.position'] = (0, 0)``.

Controlling annotation placement
---------------------------------

By default, annotations for events in the first 26 weeks of a year appear
on the left side; everything else on the right.  The layout engine
automatically shifts labels downward to avoid overlap.

You can override the automatic placement with *hint* or *side*:

.. code-block:: python

   from lifegraph.core import Point

   # Place with a positional hint (data coordinates)
   g.add_life_event("Event A", date(2006, 1, 23), color="r",
                     hint=(10, -10))

   # Force to the right side
   g.add_life_event("Event B", date(2006, 1, 23), color="r",
                     side=Side.RIGHT)

   # Era span with a hint
   g.add_era_span("Span", date(2010, 2, 1), date(2011, 8, 1),
                   color="g", hint=Point(52, 105))

Using a provided matplotlib axes
---------------------------------

For advanced layouts you can pass your own axes to ``Lifegraph`` via the
``ax`` parameter.  This lets you compose multiple life graphs on one figure
or mix life graphs with standard matplotlib plots.

When using provided axes:

1. Call :meth:`~lifegraph.Lifegraph.draw` to render instead of
   :meth:`~lifegraph.Lifegraph.show` or :meth:`~lifegraph.Lifegraph.save`.
2. Manage the figure lifecycle yourself (``fig.savefig``, ``plt.close``).

Single provided axes
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import matplotlib.pyplot as plt
   from lifegraph import Lifegraph
   from datetime import date

   fig, ax = plt.subplots(figsize=(10, 8))

   birthday = date(1990, 11, 1)
   g = Lifegraph(birthday, max_age=50, ax=ax)

   g.add_life_event("First Job", date(2012, 6, 1), color="#00FF00")
   g.add_life_event("Got Married", date(2015, 8, 15), color="#FF1493")
   g.add_life_event("Started PhD", date(2018, 9, 1), color="#1E90FF")

   g.add_title("My Life (Single Axes Example)")
   g.draw()

   fig.savefig("provided_axes_single.png", dpi=300)
   plt.close(fig)

Multiple subplots
~~~~~~~~~~~~~~~~~

.. code-block:: python

   import matplotlib.pyplot as plt
   from lifegraph import Lifegraph
   from datetime import date

   fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

   g1 = Lifegraph(date(1985, 3, 15), max_age=50, ax=ax1)
   g1.add_life_event("Graduated", date(2007, 5, 20), color="#FFD700")
   g1.add_life_event("First Child", date(2012, 3, 10), color="#FF69B4")
   g1.add_title("Person 1's Life")

   g2 = Lifegraph(date(1992, 7, 20), max_age=50, ax=ax2)
   g2.add_life_event("Career start", date(2014, 8, 1), color="#32CD32")
   g2.add_life_event("Bought House", date(2019, 11, 5), color="#8B4513")
   g2.add_title("Person 2's Life")

   g1.draw()
   g2.draw()

   plt.tight_layout()
   fig.savefig("side_by_side.png", dpi=300)
   plt.close(fig)

Mixing lifegraph with other plots
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import matplotlib.pyplot as plt
   from lifegraph import Lifegraph
   from datetime import date

   fig = plt.figure(figsize=(16, 10))

   ax1 = fig.add_subplot(2, 1, 1)
   g = Lifegraph(date(1988, 5, 10), max_age=50, ax=ax1)
   g.add_life_event("Career Change", date(2015, 1, 1), color="#FF6347")
   g.add_title("Life Timeline")
   g.draw()

   ax2 = fig.add_subplot(2, 1, 2)
   years = [2010, 2012, 2014, 2016, 2018, 2020]
   happiness = [6, 7, 5, 8, 9, 8]
   ax2.plot(years, happiness, marker="o", linewidth=2, color="#4169E1")
   ax2.set_xlabel("Year")
   ax2.set_ylabel("Happiness Level")
   ax2.set_title("Happiness Over Time")
   ax2.grid(True, alpha=0.3)

   plt.tight_layout()
   fig.savefig("mixed_plots.png", dpi=300)
   plt.close(fig)

Saving and loading configurations
---------------------------------

You can export a lifegraph to a portable JSON or YAML file and later
recreate the exact same graph from that file.  This is useful for sharing
configurations, version-controlling your life data separately from code,
or building tools on top of the format.

Exporting to JSON
~~~~~~~~~~~~~~~~~

.. code-block:: python

   g = Lifegraph(birthday, dpi=300, size=Papersize.Letter)
   g.add_life_event("Graduated", date(2012, 5, 20), color="#00FF00")
   g.add_era("College", date(2008, 9, 1), date(2012, 5, 15), color="blue")
   g.add_title("My Life")

   g.save_config("my_life.json")

The format is inferred from the file extension: ``.json`` for JSON,
``.yaml`` or ``.yml`` for YAML.

Including axis styling
~~~~~~~~~~~~~~~~~~~~~~

By default, axis label customisations are not included.  Pass
``include_styling=True`` to export them:

.. code-block:: python

   g.format_x_axis(text="Weeks", color="red", fontsize=14)
   g.save_config("my_life_styled.json", include_styling=True)

Importing from a config file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   g = Lifegraph.from_config("my_life.json")
   g.save("my_life.png")

If the file contains a ``styling`` section, it is applied by default.
Pass ``apply_styling=False`` to ignore it:

.. code-block:: python

   g = Lifegraph.from_config("my_life_styled.json", apply_styling=False)

YAML support
~~~~~~~~~~~~

YAML requires the optional ``pyyaml`` package:

.. code-block:: bash

   pip install lifegraph[yaml]

.. code-block:: python

   g.save_config("my_life.yaml")
   g2 = Lifegraph.from_config("my_life.yaml")

Putting it all together
-----------------------

Here is a complete example combining several features:

.. code-block:: python

   from lifegraph import Lifegraph, Side
   from lifegraph.configuration import Papersize
   from lifegraph.core import Point
   from datetime import date

   birthday = date(1995, 11, 20)
   g = Lifegraph(birthday, dpi=300, size=Papersize.Letter,
                  label_space_epsilon=1)

   g.add_life_event("Won an award", date(2013, 11, 20), "#014421")
   g.add_life_event("Hiked the Rockies", date(2014, 2, 14), "#DC143C",
                     hint=(25, -3))
   g.add_life_event("First marathon", date(2017, 9, 11), "#990000")
   g.add_life_event("Built a canoe", date(2018, 12, 8), "#87CEFA")
   g.add_life_event("Started at Ecosia", date(2019, 1, 7), "#00008B")

   g.add_era("Elementary School", date(2001, 8, 24), date(2007, 6, 5), "r")
   g.add_era("High School", date(2010, 8, 24), date(2014, 6, 5), "#00838f")
   g.add_era("College", date(2014, 9, 1), date(2018, 12, 14),
             (80 / 255, 0, 0), side=Side.LEFT)

   g.add_era_span("Longest vacation", date(2016, 8, 22),
                   date(2016, 12, 16), "#D2691E", hint=Point(53, 28))

   g.add_title("The Life of Someone")
   g.show_max_age_label()

   g.save("complete_life.png")
