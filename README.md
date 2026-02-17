<!-- Images -->
[alife]: examples/images/alife.png "A Life Graph"

# Life Graph
[![License](https://img.shields.io/github/license/k20shores/lifegraph.svg)](https://github.com/k20shores/lifegraph/blob/main/LICENSE)
[![Tests](https://github.com/k20shores/lifegraph/actions/workflows/test.yml/badge.svg)](https://github.com/k20shores/lifegraph/actions/workflows/test.yml)
[![codecov](https://codecov.io/github/k20shores/lifegraph/graph/badge.svg?token=H171ALNX97)](https://codecov.io/github/k20shores/lifegraph)
[![pypi version](https://img.shields.io/pypi/v/lifegraph.svg)](https://pypi.org/project/lifegraph/)

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
```python
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

## Saving and Loading Configurations

Export a lifegraph to a portable JSON or YAML file and recreate it later:

```python
# Export
g.save_config("my_life.json")
g.save_config("my_life.yaml", include_styling=True)  # requires: pip install lifegraph[yaml]

# Import
g = Lifegraph.from_config("my_life.json")
g.save("my_life.png")
```

For tutorials, API reference, and more examples, see the [full documentation](https://lifegraph.readthedocs.io/en/latest/).

# Contributing and Code of Conduct
[Read our contributing guidelines](docs/CONTRIBUTING)

[Read our code of conduct](docs/CODE_OF_CONDUCT.md)
