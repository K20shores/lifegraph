<!-- Images -->
[alife]: examples/images/alife.png "A Life Graph"
[grid]: examples/images/grid.png "A Simple Grid"
[grid_with_title]: examples/images/grid_with_title.png "With a Title"
[grid_with_watermark]: examples/images/grid_with_watermark.png "With a Watermark"
[grid_maxage]: examples/images/grid_maxage.png "Adding the max age"
[grid_life_event]: examples/images/grid_life_event.png "A life event"
[grid_era]: examples/images/grid_era.png "An era"
[grid_era_span]: examples/images/grid_era_span.png "An era span"
[grid_add_image]: examples/images/grid_add_image.png "Add an image"
[grid_customization]: examples/images/grid_customization.png "Customize the grid"
[annotation_placement]: examples/images/placement.png "Annotation placement"
[provided_axes_single]: examples/images/provided_axes_single.png "Single provided axes"
[provided_axes_multiple]: examples/images/provided_axes_multiple.png "Multiple subplots"
[provided_axes_mixed]: examples/images/provided_axes_mixed.png "Mixed plot types"

# Life Graph
[![License](https://img.shields.io/github/license/k20shores/lifegraph.svg)](https://github.com/k20shores/lifegraph/blob/main/LICENSE)
[![Tests](https://github.com/k20shores/lifegraph/actions/workflows/test.yml/badge.svg)](https://github.com/k20shores/lifegraph/actions/workflows/test.yml)
[![codecov](https://codecov.io/github/k20shores/lifegraph/graph/badge.svg?token=H171ALNX97)](https://codecov.io/github/k20shores/lifegraph)
[![PyPI version](https://badge.fury.io/py/lifegraph.svg)](https://badge.fury.io/py/lifegraph)

# Installation

```
pip install lifegraph
```

# Life Graph Inspiration
Inspired by [this post](https://waitbutwhy.com/2014/05/life-weeks.html), I decided I wanted to make my own graph of my life.
In the comments on that post, there are many other graphs available, but most of them add lots of different things that I did
not care for. They looked extremely nice, but not nearly as simple as the box of squares originally showed in the post. The simplicity
of seeing my life on a tiny grid really hit me. I wanted to recreate that.

The folks at [waitbutwhy.com](https://waitbutwhy.com) own the idea behind this work. They gave me permission to produce and realease
this code for free use by everyone else.

# A Life Graph Example
![A Life Graph][alife]

The code:
```
from lifegraph.lifegraph import Lifegraph, Papersize, random_color, Point, Side
from datetime import date, datetime

birthday = date(1995, 11, 20)
g = Lifegraph(birthday, dpi=300, size=Papersize.Letter, label_space_epsilon=1)

g.add_life_event('Won an award', date(2013, 11, 20), '#014421')
g.add_life_event('Hiked the Rocky Mountains', date(2014, 2, 14), '#DC143C', hint=(25, -3))
g.add_life_event('Ran first marathon', date(2017, 9, 11), '#990000')
g.add_life_event('Built a canoe', date(2018, 12, 8), '#87CEFA')
g.add_life_event('Started working at\nEcosia', date(2019, 1, 7), '#00008B')

now = datetime.utcnow()
g.add_life_event('Today', date(now.year, now.month, now.day), (0.75, 0, 0.75))

g.add_era("Elementary School", date(2001, 8, 24), date(2007, 6, 5), 'r')
g.add_era("Intermediate School", date(2007, 8, 24), date(2008, 6, 5), '#00838f')
g.add_era("Middle School", date(2008, 8, 24), date(2010, 6, 5), 'b')
g.add_era("High School", date(2010, 8, 24), date(2014, 6, 5), '#00838f')
g.add_era("College", date(2014, 9, 1), date(2018, 12, 14), (80/255, 0, 0), side=Side.LEFT)

g.add_era_span("Longest vacation ever", date(2016, 8, 22), date(2016, 12, 16), '#D2691E', hint=Point(53, 28))

g.add_title("The life of Someone")

g.show_max_age_label()

g.save("images/alife.png")
```

# A Simple Grid
To make a grid of squares, this is all you need.
By default, the axes instance is constrained to a smaller portion of the page to make
room for annotations on the edge of the graph. The axes_rect argument ensures that the graph
takes up more room.
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, axes_rect=[.1, .1, .8, .8])
g.save("grid.png")
```

![A simple grid][grid]

# Add a Title
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4)
g.add_title("Time is Not Equal to Money")
g.save("grid.png")
```

![Adding a title][grid_with_title]

# Add a Watermark
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4)
g.add_title("Time is Not Equal to Money")
g.add_watermark("Your Life")
g.save("grid.png")
```

![Adding a watermark][grid_with_watermark]

# Display and Change the Max Age
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)
g.add_title("Time is Not Equal to Money")
g.show_max_age_label()
g.save("images/grid_maxage.png")
```

![Changing and displaying the max age][grid_maxage]

# Adding a Life Event
You can add events of your life. The graph is initialized from your birthday and where
the events are placed on the graph is calculated from your birthdate and the day that 
the event happened. Notice the different ways that you can set the color and that
you can specify which side you'd like to place the text if you don't like the default.

```
from lifegraph.lifegraph import Lifegraph, Papersize, Side
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

g.add_title("Time is Not Equal to Money")
g.show_max_age_label()

# a random color will be chosen if you don't provide one
g.add_life_event('My first paycheck', date(2006, 8, 23))

# colors can be added as hex strings
# and you can hint at which side you want the text on
g.add_life_event('Graduated\nhighschool', date(2008, 6, 2), color="#00FF00", side=Side.LEFT)

# or RGB
g.add_life_event('First car purchased', date(2010, 7, 14), color = (1, 0, 0))

g.save("images/grid_life_event.png")
```

![Adding life events][grid_life_event]

# Adding an Era
You can color parts of your life that marked an era.
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

g.add_title("Time is Not Equal to Money")
g.show_max_age_label()

# random color will be used
g.add_era('That one thing\nI did as a kid', date(2000, 3, 4), date(2005, 8, 22))

# you can also choose the color
g.add_era('Running for city\ncouncil', date(2019, 12, 10), date(2020, 11, 5), color="#4423fe")

g.save("images/grid_era_span.png")
```

![Adding eras][grid_era]

# Adding an Era Span
Or you can use this dumbbell shape to denote eras
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

g.add_title("Time is Not Equal to Money")
g.show_max_age_label()

# random color will be used
g.add_era_span('That one thing\nI did as a kid', date(2000, 3, 4), date(2005, 8, 22))

# you can also choose the color
g.add_era_span('Running for city\ncouncil', date(2019, 12, 10), date(2020, 11, 5), color="#4423fe")

g.save("images/grid_era_span.png")
```

![Adding era spans][grid_era_span]

# Add an Image
You can add images to the axes instance.
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

g.add_title("Time is Not Equal to Money")
g.show_max_age_label()

g.add_image("couple.jpg", alpha=0.5)

g.save("images/grid_add_image.png")
```
![Adding an image][grid_add_image]

# Customize the Grid
The grid properties for each papersize is controlled by the matplotlib rc paramters. The paramters
for each papersize can be found in [the configuration file](lifegraph/configuration.py).
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

g.add_title("Time is Not Equal to Money")
g.show_max_age_label()

g.settings.rcParams["lines.marker"] = 'v'
g.settings.rcParams["lines.markersize"] = 2.0

g.save("images/grid_customization.png")
```

There are a number of other rc parameters defined for this package. There are really
too many to provide an example of each. Please see the availabel 
configurations for a better idea of what can be customized. Some of the 
customizable parameters can be set with the lifegraph. For example, `g.format_x_axis(positionx=0, positiony=0)` is equivalent to `g.settings.otherParams['xlabel.position'] = (0, 0)` (both coordinates are in axes coordinates) and would move the 'Week of the year ->' text to the bottom left of the graph.

![Customizing the grid][grid_customization]

# Annotation Placement

By default, the graph will place annotations from top to bottom. The graph lays out annotations
so that they do not overlap. If annotations do overlap, this is a bug. Please file a bug report. Annotations
for events in the first 26 weeks of a year in your life will be on the right side, everything else on the left.

However, you can control the placement if you wish through the use of the `hint` and `side` keyword arguments.

```
from lifegraph.lifegraph import Lifegraph, Papersize, Side
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

g.add_title("Time is Not Equal to Money")
g.show_max_age_label()

# the default placement
g.add_life_event('My first paycheck', date(2006, 1, 23), color='r')

# a hint, in data coordinates
g.add_life_event('My first paycheck', date(2006, 1, 23), color='r', hint=(10, -10))

# a side
g.add_life_event('My first paycheck', date(2006, 1, 23), color='r', side=Side.RIGHT)

# the default placement
g.add_era_span('Green thing', start_date=date(2010, 2, 1), end_date=date(2011, 8, 1), color='g')

# a hint, in data coordinates
g.add_era_span('Red thing', start_date=date(2012, 2, 1), end_date=date(2013, 8, 1), color='r', hint=(52, 105))

# a side
g.add_era_span('Blue thing', start_date=date(2014, 2, 1), end_date=date(2015, 8, 1), color='b', side=Side.LEFT)

g.save("images/placement.png")
```

![Annotation Placement][annotation_placement]

# Using a Provided Axes

You can pass your own matplotlib axes to Lifegraph with the `ax` parameter. This lets you
compose lifegraphs with other matplotlib plots or place multiple lifegraphs on a single figure.
When using a provided axes, call `g.draw()` to render the lifegraph, then manage the figure
lifecycle yourself.

## Single Provided Axes
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 8))

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, max_age=50, ax=ax)

g.add_life_event('First Job', date(2012, 6, 1), color='#00FF00')
g.add_life_event('Got Married', date(2015, 8, 15), color='#FF1493')
g.add_life_event('Started PhD', date(2018, 9, 1), color='#1E90FF')

g.add_title("My Life (Single Axes Example)")
g.draw()

fig.savefig("provided_axes_single.png", dpi=300)
plt.close(fig)
```

![Single provided axes][provided_axes_single]

## Multiple Subplots
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

g1 = Lifegraph(date(1985, 3, 15), max_age=50, ax=ax1)
g2 = Lifegraph(date(1992, 7, 20), max_age=50, ax=ax2)

g1.add_life_event('Graduated College', date(2007, 5, 20), color='#FFD700')
g1.add_life_event('First Child', date(2012, 3, 10), color='#FF69B4')
g1.add_title("Person 1's Life")

g2.add_life_event('Started Career', date(2014, 8, 1), color='#32CD32')
g2.add_life_event('Bought House', date(2019, 11, 5), color='#8B4513')
g2.add_title("Person 2's Life")

g1.draw()
g2.draw()

plt.tight_layout()
fig.savefig("provided_axes_multiple.png", dpi=300)
plt.close(fig)
```

![Multiple subplots][provided_axes_multiple]

## Mixing Lifegraph with Other Plots
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(16, 10))

ax1 = fig.add_subplot(2, 1, 1)
g = Lifegraph(date(1988, 5, 10), max_age=50, ax=ax1)
g.add_life_event('Career Change', date(2015, 1, 1), color='#FF6347')
g.add_title("Life Timeline")
g.draw()

ax2 = fig.add_subplot(2, 1, 2)
years = [2010, 2012, 2014, 2016, 2018, 2020]
happiness = [6, 7, 5, 8, 9, 8]
ax2.plot(years, happiness, marker='o', linewidth=2, color='#4169E1')
ax2.set_xlabel('Year')
ax2.set_ylabel('Happiness Level')
ax2.set_title('Happiness Over Time')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
fig.savefig("provided_axes_mixed.png", dpi=300)
plt.close(fig)
```

![Mixed plot types][provided_axes_mixed]

# Contributing and Code of Conduct
[Read our contributing guidelines](docs/CONTRIBUTING)

[Read our code of conduct](docs/CODE_OF_CONDUCT.md)