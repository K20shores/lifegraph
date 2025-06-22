import random
from matplotlib import colors as mcolors

exclude = []
colors = [(key, val)
          for key, val in mcolors.BASE_COLORS.items() if val not in exclude]
for key, val in mcolors.CSS4_COLORS.items():
    if val not in exclude:
        colors.append((key, val))

def random_color():
    """Returns a random color defined in matplotlib.colors.BASE_COLORS or matplotlib.colors.CSS4_COLORS"""
    c = random.choice(colors)
    return c[1]
