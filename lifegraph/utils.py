import random
from matplotlib import colors as mcolors

exclude = []
colors = [(key, val)
          for key, val in mcolors.BASE_COLORS.items() if val not in exclude]
for key, val in mcolors.CSS4_COLORS.items():
    if val not in exclude:
        colors.append((key, val))

def random_color():
    """Returns a random color defined in matplotlib.colors.BASE_COLORS or matpotlib.colors.CSS4_COLORS"""
    c = colors[random.randint(0, len(colors) - 1)]
    return c[1]
