"""
Changing the Maximum Age
========================

The grid has 90 rows by default. Set ``max_age`` to change it, and
``show_max_age_label()`` to display the number at the bottom.
"""

# %%

from datetime import date

from lifegraph import Lifegraph
from lifegraph.configuration import Papersize

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)
g.add_title("Time is Not Equal to Money")
g.show_max_age_label()
g.save("grid_maxage.png")
