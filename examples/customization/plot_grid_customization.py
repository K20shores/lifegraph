"""
Grid Style
==========

Override the default marker shape, size, and axis labels through
``g.settings.rcParams``.
"""

# %%

from datetime import date

from lifegraph import Lifegraph
from lifegraph.configuration import Papersize

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

g.add_title("Time is Not Equal to Money")
g.show_max_age_label()

g.settings.rcParams["lines.marker"] = "v"
g.settings.rcParams["lines.markersize"] = 2.0

g.save("grid_customization.png")
