from enum import Enum

class Side(Enum):
    """Visually indicates the left or right of the plot"""
    LEFT = 1
    RIGHT = 2

class Point:
    """A point class that holds the x and y coordinates in data units"""
    def __init__(self, x, y):
        """ Initialize the Point class

        :param x: The x coordinate
        :param y: The y coordinate

        """
        self.x = x
        self.y = y
    def __repr__(self):
        """Print a description of the Point class"""
        return f"({self.x}, {self.y})"
    def __str__(self):
        """Print a description of the Point class"""
        return f"({self.x}, {self.y})"

class DatePosition(Point):
    """A class to hold the week, year of life, and date assocaited with a Point"""
    def __init__(self, x, y, date):
        """Initialize the DatePosition class. The base class is a Point

        :param x: x coordinate passsed to Point class
        :param y: y coordinate passsed to Point class
        :param date: The date associated with the position

        """
        super().__init__(x, y)
        self.date = date
    def __repr__(self):
        """Print a description of the DatePosition class"""
        return f"DatePosition: year({self.y}), week({self.x}), date({self.date}) at point {super().__repr__()}"
    def __str__(self):
        """Print a description of the DatePosition class"""
        return f"DatePosition: year({self.y}), week({self.x}), date({self.date}) at point {super().__repr__()}"

class Marker(Point):
    """A class to indicate how and where to draw a marker"""
    def __init__(self, x, y, marker='s', fillstyle='none', color='black'):
        """A class to configure the marker on the graph. The base is a Point class

        :param x: The x position of a marker
        :param y: The y position of a marker
        :param marker: (Default value = 's') A matplotlib marker
        :param fillstyle: (Default value = 'none') A matplotlib fillstyle
        :param color: (Default value = 'black') A matplotlib color

        """
        super().__init__(x, y)
        self.marker = marker
        self.fillstyle = fillstyle
        self.color = color
    def __repr__(self):
        """Print a description of the Marker class"""
        return f"Marker at {super().__repr__()}"
    def __str__(self):
        """Print a description of the Marker class"""
        return f"Marker at {super().__repr__()}"

class Annotation(Point):
    """A class to hold the text of an annotation with methods to help layout the text."""
    def __init__(self, date, text, label_point, color='black', bbox=None, event_point=None, put_circle_around_point=True, marker=None, relpos=(.5, .5)):
        """Initialize the Annotation class. THe base is a Point class.

        :param date: When the event occurred
        :param text: The label text of the annotation
        :param label_point: The location of the label text
        :param color: (Default value = 'black') A matplotlib color
        :param bbox: (Default value = None) The bounding box of the point
        :param event_point: (Default value = None) Where on the graph the event is located
        :param put_circle_around_point: (Default value = True) Should the event point be circled on the graph
        :param shrink: (Default value = 0) How much from the event point should the arrow stop
        :param marker: (Default value = None) A Marker class
        :param relpos: (Default value = (.5, .5)) The position that the annotation arrow innitates from on the label, see https://matplotlib.org/tutorials/text/annotations.html

        """
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
        """Set the bounding box of an annotation

        :param bbox: a matplotlib.transforms.Bbox instance

        """
        self.bbox = bbox
    def set_relpos(self, relpos):
        """Set the relative position that the arrow should draw from

        see https://matplotlib.org/tutorials/text/annotations.html

        :param relpos: a tuple whose values range from [0, 1]

        """
        self.relpos = relpos
    def overlaps(self, that):
        """Check that the two Bboxes don't overlap
        
        They don't overlap if
            1) one rectangle's left side is strictly to the right other's right side
            2) one rectangle's top side is stricly bellow the other's bottom side

        :param that: an Annotation

        """
        if (not isinstance(that, Annotation)):
            raise ValueError("Argument for intersects should be an annotation")
        if (self.bbox.xmin >= that.bbox.xmax or that.bbox.xmin >= self.bbox.xmax):
            return False
        if (self.bbox.ymin >= that.bbox.ymax or that.bbox.ymin >= self.bbox.ymax):
            return False
        return True
    def is_within_epsilon_of(self, that, epsilon):
        """Check that the two are not at least as close as some epsilon

        :param that: An Annotation
        :param epsilon: A real number to define the tolerance for how close the label text can be

        """
        if (not isinstance(that, Annotation)):
            raise ValueError("Argument for intersects should be an annotation")
        if (self.bbox.xmin - epsilon > that.bbox.xmax or that.bbox.xmin - epsilon > self.bbox.xmax):
            return False
        if (self.bbox.ymin - epsilon > that.bbox.ymax or that.bbox.ymin - epsilon > self.bbox.ymax):
            return False
        return True
    def get_bbox_overlap(self, that, epsilon):
        """Detmerine by how much the two annotation bounding boxes overlap

        :param that: an Annotation
        :param epsilon: A real number that will add a buffer space between the two label text bounding boxes

        """
        if (not isinstance(that, Annotation)):
            raise ValueError("Argument for intersects should be an annotation")
        width = min(self.bbox.xmax, that.bbox.xmax) - max(self.bbox.xmin, that.bbox.xmin)
        height = min(self.bbox.ymax, that.bbox.ymax) - max(self.bbox.ymin, that.bbox.ymin)
        height = abs(that.bbox.ymax - self.bbox.ymin) + epsilon
        return (width, height)
    def get_xy_correction(self, that, epsilon):
        """Detmerine by how much the two annotation bounding boxes overlap

        :param that: an Annotation
        :param epsilon: A real number that will add a buffer space between the two label text bounding boxes

        """
        if (not isinstance(that, Annotation)):
            raise ValueError("Argument for intersects should be an annotation")
        width = abs(that.bbox.xmax - self.bbox.xmin) + epsilon
        height = abs(that.bbox.ymax - self.bbox.ymin) + epsilon
        return (width, height)
    def update_X_with_correction(self, correction):
        """Move the label text in the x direction according to the value in correction

        :param correction: a tuple of real number where correction[0] determines by how much the x position of the label should move

        """
        self.x += correction[0]
        self.bbox.x0 += correction[0]
        self.bbox.x1 += correction[0]
    def update_Y_with_correction(self, correction):
        """Move the label text in the y direction according to the value in correction

        :param correction: a tuple of real number where correction[1] determines by how much the y position of the label should move

        """
        self.y += correction[1]
        self.bbox.y0 += correction[1]
        self.bbox.y1 += correction[1]
    def __repr__(self):
        """Print a description of the Annotation class"""
        return f"Annotation '{self.text}' at {super().__repr__()}"
    def __str__(self):
        """Print a description of the Annotation class"""
        return f"Annotation '{self.text}' at {super().__repr__()}"

class Era():
    """A class which shows a highlighted area on the graph to indicate a span of time"""
    def __init__(self, text, start, end, color, alpha=1):
        """Initialize the Era class

        :param text: The text to place on the graph
        :param start: A datetime.date indicating the start of the era
        :param end: A datetime.date indicating the end of the era
        :param color: A color useable by any matplotlib object
        :param alpha: (Default value = 1)

        """
        self.text = text
        self.start = start
        self.end = end
        self.color = color
        self.alpha = alpha
    def __repr__(self):
        """Print a description of the Era class"""
        return f"Era '{self.text}' starting at {self.start}, ending at {self.end}"
    def __str__(self):
        """Print a description of the Era class"""
        return f"Era '{self.text}' starting at {self.start}, ending at {self.end}"

class EraSpan(Era):
    """A class which shows a dumbbell shape on the graph defining a span of your life"""
    def __init__(self, text, start, end, color, start_marker=None, end_marker=None):
        """Initalize the Era span class. The base is an Era.

        :param text: The text to place on the graph
        :param start: A datetime.date indicating the start of the era
        :param end: A datetime.date indicating the end of the era
        :param color: A color useable by any matplotlib object
        :param start_marker: (Default = None) A marker for the starting point if one is wanted different than the default of the graph
        :param end_marker: (Default = None) A marker for the ending point if one is wanted different than the default of the graph

        """
        super().__init__(text, start, end, color)
        self.start_marker = start_marker
        self.end_marker = end_marker
