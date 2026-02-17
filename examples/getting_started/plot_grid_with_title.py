"""
Adding a Title
==============

Place text above the grid.
"""

# %%
# Use :meth:`~lifegraph.Lifegraph.add_title` to add a heading.

from datetime import date

from lifegraph import Lifegraph
from lifegraph.configuration import Papersize

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4)
g.add_title("Time is Not Equal to Money")
g.save("grid_with_title.png")
