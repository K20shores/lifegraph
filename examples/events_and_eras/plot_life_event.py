"""
Life Events
===========

A life event is a labeled point on the grid. Colors can be hex strings,
RGB tuples, or named colors. Use ``side`` to force label placement.
"""

# %%

from datetime import date

from lifegraph import Lifegraph, Side
from lifegraph.configuration import Papersize

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

g.add_title("Time is Not Equal to Money")
g.show_max_age_label()

# a random color will be chosen if you don't provide one
g.add_life_event("My first paycheck", date(2006, 8, 23))

# colors can be hex strings; use side= to control label placement
g.add_life_event("Graduated\nhighschool", date(2008, 6, 2), color="#00FF00", side=Side.LEFT)

# or RGB tuples
g.add_life_event("First car purchased", date(2010, 7, 14), color=(1, 0, 0))

g.save("grid_life_event.png")
