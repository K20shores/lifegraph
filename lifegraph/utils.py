import random
from matplotlib import colors as mcolors

exclude = []
colors = [(key, val)
          for key, val in mcolors.BASE_COLORS.items() if val not in exclude]
for key, val in mcolors.CSS4_COLORS.items():
    if val not in exclude:
        colors.append((key, val))

def random_color():
    """Return a random color from matplotlib's named color sets.

    Selects a random color from the union of
    :data:`matplotlib.colors.BASE_COLORS` and
    :data:`matplotlib.colors.CSS4_COLORS`.

    Returns
    -------
    str or tuple
        A color value accepted by matplotlib (e.g. ``'red'`` or
        ``(1.0, 0.0, 0.0)``).

    Examples
    --------
    >>> from lifegraph.utils import random_color
    >>> c = random_color()
    """
    c = random.choice(colors)
    return c[1]
