from enum import Enum

class Side(Enum):
    """Specify which side of the plot to place an annotation.

    Use ``Side.LEFT`` to place the label to the left of the grid or
    ``Side.RIGHT`` to place it to the right.

    Examples
    --------
    >>> from lifegraph import Lifegraph, Side
    >>> from datetime import date
    >>> g = Lifegraph(date(1990, 1, 1))
    >>> g.add_life_event("Event", date(2000, 6, 1), side=Side.LEFT)
    """
    LEFT = 1
    RIGHT = 2

class Point:
    """A 2-D point in data coordinates.

    Parameters
    ----------
    x : float
        The x coordinate.
    y : float
        The y coordinate.

    Examples
    --------
    >>> from lifegraph.core import Point
    >>> p = Point(10, 20)
    >>> p.x
    10
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x}, {self.y})"
    def __str__(self):
        return f"({self.x}, {self.y})"

class DatePosition(Point):
    """A point on the grid associated with a calendar date.

    Extends :class:`Point` to additionally store the date that maps to the
    ``(week, year_of_life)`` grid coordinate.

    Parameters
    ----------
    x : int
        Week number (1--52).
    y : int
        Year of life (0-indexed from birthdate).
    date : datetime.date
        The calendar date this position represents.

    Examples
    --------
    >>> from lifegraph.core import DatePosition
    >>> from datetime import date
    >>> dp = DatePosition(10, 5, date(1995, 3, 1))
    >>> dp.date
    datetime.date(1995, 3, 1)
    """
    def __init__(self, x, y, date):
        super().__init__(x, y)
        self.date = date
    def __repr__(self):
        return f"DatePosition: year({self.y}), week({self.x}), date({self.date}) at point {super().__repr__()}"
    def __str__(self):
        return f"DatePosition: year({self.y}), week({self.x}), date({self.date}) at point {super().__repr__()}"

class Marker(Point):
    """Configuration for a colored marker drawn on the grid.

    Extends :class:`Point` with matplotlib marker styling attributes.

    Parameters
    ----------
    x : float
        The x position of the marker.
    y : float
        The y position of the marker.
    marker : str, optional
        A matplotlib marker style. Default is ``'s'`` (square).
    fillstyle : str, optional
        A matplotlib fill style. Default is ``'none'``.
    color : str or tuple, optional
        A matplotlib color. Default is ``'black'``.

    Examples
    --------
    >>> from lifegraph.core import Marker
    >>> m = Marker(5, 10, color='red')
    """
    def __init__(self, x, y, marker='s', fillstyle='none', color='black'):
        super().__init__(x, y)
        self.marker = marker
        self.fillstyle = fillstyle
        self.color = color
    def __repr__(self):
        return f"Marker at {super().__repr__()}"
    def __str__(self):
        return f"Marker at {super().__repr__()}"

class Annotation(Point):
    """A text annotation with layout-conflict resolution support.

    Holds the label text and its position, along with metadata used by
    :class:`~lifegraph.lifegraph.Lifegraph` to prevent overlapping labels.

    Parameters
    ----------
    date : datetime.date
        When the annotated event occurred.
    text : str
        The label text.
    label_point : Point
        Initial location for the label text.
    color : str or tuple, optional
        A matplotlib color. Default is ``'black'``.
    bbox : matplotlib.transforms.Bbox or None, optional
        The bounding box of the rendered text. Set after layout.
    event_point : Point or None, optional
        Where on the grid the event is located.
    put_circle_around_point : bool, optional
        Whether to draw a circle around the event square. Default is ``True``.
    marker : Marker or None, optional
        A :class:`Marker` to draw at the event position.
    relpos : tuple of float, optional
        The relative position on the label from which the annotation arrow
        originates. See `matplotlib annotation guide
        <https://matplotlib.org/tutorials/text/annotations.html>`_.
        Default is ``(0.5, 0.5)``.
    """
    def __init__(self, date, text, label_point, color='black', bbox=None, event_point=None, put_circle_around_point=True, marker=None, relpos=(.5, .5)):
        super().__init__(label_point.x, label_point.y)
        self.date = date
        self.text = text
        self.color = color
        self.bbox = bbox
        self.event_point = event_point
        self.put_circle_around_point = put_circle_around_point
        self.marker = marker
        self.relpos = relpos
    def set_bbox(self, bbox):
        """Set the bounding box of the rendered annotation text.

        Parameters
        ----------
        bbox : matplotlib.transforms.Bbox
            The bounding box in data coordinates.
        """
        self.bbox = bbox
    def set_relpos(self, relpos):
        """Set the arrow origin relative to the label bounding box.

        Parameters
        ----------
        relpos : tuple of float
            ``(rx, ry)`` where each value is in ``[0, 1]``. See the
            `matplotlib annotation guide
            <https://matplotlib.org/tutorials/text/annotations.html>`_.
        """
        self.relpos = relpos
    def overlaps(self, that):
        """Check whether this annotation's bounding box overlaps another's.

        Two boxes do *not* overlap when one is entirely to the right of the
        other, or entirely below the other.

        Parameters
        ----------
        that : Annotation
            The other annotation to test against.

        Returns
        -------
        bool
            ``True`` if the bounding boxes overlap.

        Raises
        ------
        ValueError
            If *that* is not an :class:`Annotation`.
        """
        if (not isinstance(that, Annotation)):
            raise ValueError("Argument for intersects should be an annotation")
        if (self.bbox.xmin >= that.bbox.xmax or that.bbox.xmin >= self.bbox.xmax):
            return False
        if (self.bbox.ymin >= that.bbox.ymax or that.bbox.ymin >= self.bbox.ymax):
            return False
        return True
    def is_within_epsilon_of(self, that, epsilon):
        """Check whether two annotations are closer than a tolerance.

        Parameters
        ----------
        that : Annotation
            The other annotation.
        epsilon : float
            Minimum allowed distance between bounding boxes.

        Returns
        -------
        bool
            ``True`` if the annotations are within *epsilon* of each other.

        Raises
        ------
        ValueError
            If *that* is not an :class:`Annotation`.
        """
        if (not isinstance(that, Annotation)):
            raise ValueError("Argument for intersects should be an annotation")
        if (self.bbox.xmin - epsilon > that.bbox.xmax or that.bbox.xmin - epsilon > self.bbox.xmax):
            return False
        if (self.bbox.ymin - epsilon > that.bbox.ymax or that.bbox.ymin - epsilon > self.bbox.ymax):
            return False
        return True
    def get_bbox_overlap(self, that, epsilon):
        """Compute the overlap dimensions between two annotation bounding boxes.

        Parameters
        ----------
        that : Annotation
            The other annotation.
        epsilon : float
            Buffer added to the height calculation.

        Returns
        -------
        tuple of float
            ``(width, height)`` of the overlap region.

        Raises
        ------
        ValueError
            If *that* is not an :class:`Annotation`.
        """
        if (not isinstance(that, Annotation)):
            raise ValueError("Argument for intersects should be an annotation")
        width = min(self.bbox.xmax, that.bbox.xmax) - max(self.bbox.xmin, that.bbox.xmin)
        height = min(self.bbox.ymax, that.bbox.ymax) - max(self.bbox.ymin, that.bbox.ymin)
        height = abs(that.bbox.ymax - self.bbox.ymin) + epsilon
        return (width, height)
    def get_xy_correction(self, that, epsilon):
        """Compute the correction needed to resolve an overlap.

        Parameters
        ----------
        that : Annotation
            The other annotation.
        epsilon : float
            Buffer added to the correction.

        Returns
        -------
        tuple of float
            ``(dx, dy)`` correction to apply.

        Raises
        ------
        ValueError
            If *that* is not an :class:`Annotation`.
        """
        if (not isinstance(that, Annotation)):
            raise ValueError("Argument for intersects should be an annotation")
        width = abs(that.bbox.xmax - self.bbox.xmin) + epsilon
        height = abs(that.bbox.ymax - self.bbox.ymin) + epsilon
        return (width, height)
    def update_X_with_correction(self, correction):
        """Shift the label in the x direction.

        Parameters
        ----------
        correction : tuple of float
            ``correction[0]`` is added to the x position and bounding box.
        """
        self.x += correction[0]
        self.bbox.x0 += correction[0]
        self.bbox.x1 += correction[0]
    def update_Y_with_correction(self, correction):
        """Shift the label in the y direction.

        Parameters
        ----------
        correction : tuple of float
            ``correction[1]`` is added to the y position and bounding box.
        """
        self.y += correction[1]
        self.bbox.y0 += correction[1]
        self.bbox.y1 += correction[1]
    def __repr__(self):
        return f"Annotation '{self.text}' at {super().__repr__()}"
    def __str__(self):
        return f"Annotation '{self.text}' at {super().__repr__()}"

class Era():
    """A highlighted region on the grid representing a period of time.

    Eras are drawn as colored rectangles spanning from ``start`` to ``end``
    behind the grid squares.

    Parameters
    ----------
    text : str
        Label for the era.
    start : datetime.date
        Start date of the era.
    end : datetime.date
        End date of the era.
    color : str or tuple
        A matplotlib color.
    alpha : float, optional
        Opacity of the era rectangle. Default is ``1``.

    Examples
    --------
    >>> from lifegraph import Lifegraph
    >>> from datetime import date
    >>> g = Lifegraph(date(1990, 1, 1))
    >>> g.add_era("College", date(2008, 9, 1), date(2012, 5, 15), color="blue")
    """
    def __init__(self, text, start, end, color, alpha=1):
        self.text = text
        self.start = start
        self.end = end
        self.color = color
        self.alpha = alpha
    def __repr__(self):
        return f"Era '{self.text}' starting at {self.start}, ending at {self.end}"
    def __str__(self):
        return f"Era '{self.text}' starting at {self.start}, ending at {self.end}"

class EraSpan(Era):
    """A dumbbell-shaped annotation marking a span of time.

    Draws circles at the start and end positions connected by a line,
    with an optional label.

    Parameters
    ----------
    text : str
        Label for the era span.
    start : datetime.date
        Start date.
    end : datetime.date
        End date.
    color : str or tuple
        A matplotlib color.
    start_marker : Marker or None, optional
        Custom marker for the start position.
    end_marker : Marker or None, optional
        Custom marker for the end position.

    Examples
    --------
    >>> from lifegraph import Lifegraph
    >>> from datetime import date
    >>> g = Lifegraph(date(1990, 1, 1))
    >>> g.add_era_span("Grad school", date(2012, 9, 1), date(2016, 5, 15),
    ...               color="#4423fe")
    """
    def __init__(self, text, start, end, color, start_marker=None, end_marker=None):
        super().__init__(text, start, end, color)
        self.start_marker = start_marker
        self.end_marker = end_marker
