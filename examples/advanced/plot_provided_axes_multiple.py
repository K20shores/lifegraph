"""
Provided Axes -- Multiple Subplots
===================================

Compare two life graphs side by side using matplotlib subplots.
"""

# %%

import matplotlib.pyplot as plt

from datetime import date

from lifegraph import Lifegraph

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

g1 = Lifegraph(date(1985, 3, 15), max_age=50, ax=ax1)
g1.add_life_event("Graduated College", date(2007, 5, 20), color="#FFD700")
g1.add_life_event("First Child", date(2012, 3, 10), color="#FF69B4")
g1.add_title("Person 1's Life")

g2 = Lifegraph(date(1992, 7, 20), max_age=50, ax=ax2)
g2.add_life_event("Started Career", date(2014, 8, 1), color="#32CD32")
g2.add_life_event("Bought House", date(2019, 11, 5), color="#8B4513")
g2.add_title("Person 2's Life")

g1.draw()
g2.draw()

plt.tight_layout()
fig.savefig("provided_axes_multiple.png", dpi=300, bbox_inches="tight")
