"""
Eras
====

Eras shade a rectangular region of the grid behind the squares.
"""

# %%

from datetime import date

from lifegraph import Lifegraph
from lifegraph.configuration import Papersize

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

g.add_title("Time is Not Equal to Money")
g.show_max_age_label()

# random color will be used
g.add_era("That one thing\nI did as a kid", date(2000, 3, 4), date(2005, 8, 22))

# you can also choose the color
g.add_era("Running for city\ncouncil", date(2019, 12, 10), date(2020, 11, 5), color="#4423fe")

g.save("grid_era.png")
