"""
LifeGraph
=========

A Python package for visualizing your life as a grid of weeks.

Inspired by the `Wait But Why <https://waitbutwhy.com/2014/05/life-weeks.html>`_
blog post, lifegraph lets you create a poster-sized chart where each square
represents one week of your life, with support for annotated events, colored
eras, and custom styling.

Examples
--------
>>> from lifegraph import Lifegraph, Side
>>> from datetime import date
>>> g = Lifegraph(date(1990, 1, 1))
>>> g.add_life_event("Started college", date(2008, 8, 25), color="blue")
>>> g.save("my_life.png")
"""

__version__ = "0.3.0"

from .lifegraph import Lifegraph as Lifegraph, Side as Side
