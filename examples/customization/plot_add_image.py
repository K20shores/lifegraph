"""
Image Overlay
=============

Overlay an image that fills the grid area.
"""

# %%

from datetime import date
from pathlib import Path

from lifegraph import Lifegraph
from lifegraph.configuration import Papersize

birthday = date(1990, 11, 1)

# sphinx-gallery runs scripts via exec() so __file__ is not defined;
# it does set the CWD to the script's source directory.
try:
    _here = Path(__file__).resolve().parent
except NameError:
    _here = Path.cwd()
image_path = str(_here.parent / "couple.jpg")

g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

g.add_title("Time is Not Equal to Money")
g.show_max_age_label()

g.add_image(image_path, alpha=0.5)

g.save("grid_add_image.png")
