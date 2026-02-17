"""
Label Placement
===============

Control where annotation labels appear using ``side`` or ``hint``.
"""

# %%

from datetime import date

from lifegraph import Lifegraph, Side
from lifegraph.configuration import Papersize

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

g.add_title("Time is Not Equal to Money")
g.show_max_age_label()

# default placement
g.add_life_event("My first paycheck", date(2006, 1, 23), color="r")

# a hint, in data coordinates
g.add_life_event("My first paycheck", date(2006, 1, 23), color="r", hint=(10, -10))

# force to a side
g.add_life_event("My first paycheck", date(2006, 1, 23), color="r", side=Side.RIGHT)

# era spans accept hints and sides too
g.add_era_span("Green thing", start_date=date(2010, 2, 1), end_date=date(2011, 8, 1), color="g")
g.add_era_span("Red thing", start_date=date(2012, 2, 1), end_date=date(2013, 8, 1), color="r", hint=(52, 105))
g.add_era_span("Blue thing", start_date=date(2014, 2, 1), end_date=date(2015, 8, 1), color="b", side=Side.LEFT)

g.save("placement.png")
