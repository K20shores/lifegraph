"""
Basic Grid
==========

Every square represents one week of your life.
"""

# %%
# Create a minimal life graph -- just the grid, no decorations.

from datetime import date

from lifegraph import Lifegraph
from lifegraph.configuration import Papersize

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, axes_rect=[0.1, 0.1, 0.8, 0.8])
g.save("grid.png")
