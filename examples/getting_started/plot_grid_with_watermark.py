"""
Adding a Watermark
==================

Overlay faint diagonal text across the grid.
"""

# %%
# Use :meth:`~lifegraph.Lifegraph.add_watermark` after adding a title.

from datetime import date

from lifegraph import Lifegraph
from lifegraph.configuration import Papersize

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4)
g.add_title("Time is Not Equal to Money")
g.add_watermark("Your Life")
g.save("grid_with_watermark.png")
