from dateutil.relativedelta import relativedelta
from enum import Enum
from matplotlib import colors as mcolors
from matplotlib.transforms import Bbox
import datetime
import matplotlib.image as mpimg
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
import random

from lifegraph.configuration import LifegraphParams, Papersize

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

        # the coordinates are inverted, so y0 is larger than y1
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

        # find the width and height of the overlapping rectangle
        width = min(self.bbox.xmax, that.bbox.xmax) - \
            max(self.bbox.xmin, that.bbox.xmin)
        height = min(self.bbox.ymax, that.bbox.ymax) - \
            max(self.bbox.ymin, that.bbox.ymin)

        height = abs(that.bbox.ymax - self.bbox.ymin) + epsilon

        return (width, height)

    def get_xy_correction(self, that, epsilon):
        """Detmerine by how much the two annotation bounding boxes overlap

        :param that: an Annotation
        :param epsilon: A real number that will add a buffer space between the two label text bounding boxes

        """
        if (not isinstance(that, Annotation)):
            raise ValueError("Argument for intersects should be an annotation")

        # IDK, what to do about the width
        # this will really be situational depending on the side of the
        # graph that we are on
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


class Lifegraph:
    """This class will represent your life as a graph of boxes"""

    def __init__(self, birthdate, size=Papersize.A3, dpi=300, label_space_epsilon=0.2, max_age=90, axes_rect = [.25, .1, .5, .8]):
        """Initalize the life graph

        :param birthdate: The date to start the graph from
        :param size:  (Default value = Papersize.A3) A papersize in inches
        :param dpi: (Default value = 300) Dots per inch
        :param label_space_epsilon: (Default value = .2) The minimum amount of space allowed between annotation text objects
        :param max_age: (Default value = 90) The ending age of the graph
        :param axes_rect: (Default value = [.25, .1, .5, .8]) The dimensions [left, bottom, width, height] of the axes instance passed to matplotlib.figure.Figure.add_axes

        """
        if birthdate is None or not isinstance(birthdate, datetime.date):
            raise ValueError("birthdate must be a valid datetime.date object")

        self.birthdate = birthdate

        self.settings = LifegraphParams(size)
        self.settings.rcParams["figure.dpi"] = dpi
        self.axes_rect = axes_rect

        self.renderer = None

        # the data limits, we want a grid of 52 weeks by 90 years
        # negative minimum so that ths squares are not cut off
        self.xmin = -.5
        self.xmax = 52
        self.ymin = -.5
        self.ymax = max_age

        self.xlims = [self.xmin, self.xmax]
        self.ylims = [self.ymin, self.ymax]

        self.draw_max_age = False

        self.title = None

        self.image_name = None
        self.image_alpha = 1

        self.xaxis_label = r'Week of the Year $\longrightarrow$'

        self.yaxis_label = r'$\longleftarrow$ Age'

        self.watermark_text = None

        self.label_space_epsilon = label_space_epsilon

        self.annotations = []
        self.eras = []
        self.era_spans = []

    #region Public drawing methods
    def format_x_axis(self, text=None, positionx=None, positiony=None, color=None, fontsize=None):
        """Format the x axis. This method is required.

        :param text: (Default value = None), If present, changes the text of the x-axis
        :param positionx: (Default value = None) If present, changes the location of the x postion of the x-axis (in axes coordaintes)
        :param positiony: (Default value = None) If present, changes the location of the y postion of the x-axis (in axes coordaintes)
        :param color: (Default value = None) A matplotlib color
        :param fontsize: (Default value = None) A matplotlib fontsize

        """
        if text is not None:
            self.xaxis_label = text

        x, y = self.settings.otherParams["xlabel.position"]
        if positionx is not None:
            x = positionx
        if positiony is not None:
            y = positiony
        self.settings.otherParams["xlabel.position"] = (x, y)

        if color is not None:
            self.settings.otherParams["xlabel.color"] = color

        if fontsize is not None:
            self.settings.otherParams["xlabel.fontsize"] = fontsize

    def format_y_axis(self, text=None, positionx=None, positiony=None, color=None, fontsize=None):
        """Format the y axis. This method is required.

        :param text: (Default value = None), If present, changes the text of the y-axis
        :param positionx: (Default value = None) If present, changes the location of the x postion of the y-axis (in axes coordaintes)
        :param positiony: (Default value = None) If present, changes the location of the y postion of the y-axis (in axes coordaintes)
        :param color: (Default value = None) A matplotlib color
        :param fontsize: (Default value = None) A matplotlib fontsize

        """
        if text is not None:
            self.xaxis_label = text

        x, y = self.settings.otherParams["ylabel.position"]
        if positionx is not None:
            x = positionx
        if positiony is not None:
            y = positiony
        self.settings.otherParams["ylabel.position"] = (x, y)

        if color is not None:
            self.settings.otherParams["ylabel.color"] = color

        if fontsize is not None:
            self.settings.otherParams["ylabel.fontsize"] = fontsize

    def show_max_age_label(self):
        """Places the max age on the bottom right of the plot"""
        self.draw_max_age = True

    def add_life_event(self, text, date, color=None, hint=None, side=None, color_square=True):
        """Label an event in your life

        :param text: The text the should appear for the life event
        :param date: (Default value = None) When the event occurred
        :param color: (Default value = None) A color useable by any matplotlib object
        :param hint: (Default value = None) Mutually exclusive with side. Not required. If the default placement is not desired. A Point may be provided to help the graph decide where to place the label of the event.
        :param side: (Default value = None) Mutually exclusive with hint. Not required. If not provided, the side is determined by the date. If provided, this value will put the label on the given side of the plot
        :param color_square: (Default value = True) Colors the sqaure on the graph the same color as the text if True. The sqaure is the default color of the graph squares otherwise

        """
        if (date < self.birthdate or date > (relativedelta(years=self.ymax) + self.birthdate)):
            raise ValueError(
                f"The event date must be a valid datetime.date object that is at least as recent as the birthdate and no larger than {self.ymax}")

        position = self.__to_date_position(date)

        if color is None:
            color = random_color()

        default_x = self.xmax if (position.x >= self.xmax / 2) else 0
        label_point = self.__get_label_point(hint, side, default_x, position.y)

        marker = None
        if color_square:
            marker = Marker(position.x, position.y, color=color)

        a = Annotation(date, text, label_point=label_point, color=color,
                       event_point=Point(position.x, position.y), marker=marker)
        self.annotations.append(a)

    def add_era(self, text, start_date, end_date, color=None, side=None, alpha=0.3):
        """Color in a section of your life

        :param text: The label text for the era
        :param start_date: When the event started
        :param end_date: When the event ended
        :param color: A color useable by any matplotlib object
        :param side: (Default value = None) Mutually exclusive with hint. Not required. If not provided, the side is determined by the date. If provided, this value will put the label on the given side of the plot
        :param alpha: (Default value = 0.3) the alpha value of the color

        """
        if (start_date < self.birthdate or start_date > (relativedelta(years=self.ymax) + self.birthdate)):
            raise ValueError(
                f"The event date must be a valid datetime.date object that is at least as recent as the birthdate and no larger than {self.ymax}")
        if (end_date < self.birthdate or end_date > (relativedelta(years=self.ymax) + self.birthdate)):
            raise ValueError(
                f"The event date must be a valid datetime.date object that is at least as recent as the birthdate and no larger than {self.ymax}")

        start_position = self.__to_date_position(start_date)
        end_position = self.__to_date_position(end_date)

        if color is None:
            color = random_color()

        self.eras.append(
            Era(text, start_position, end_position, color, alpha=alpha))

        label_point = self.__get_label_point(
            hint=None, side=side, default_x=self.xmax, default_y=np.average((start_position.y, end_position.y)), is_Era=True)
        # when sorting the annotation the date is used
        # choose the middle date so that the annotation ends up
        # as close to the middle of the era as possible
        # if no hint was provided
        middle_date = start_date + (end_date - start_date)/2

        a = Annotation(middle_date, text, label_point=label_point, color=color,
                       event_point=label_point, put_circle_around_point=False)
        self.annotations.append(a)

    def add_era_span(self, text, start_date, end_date, color=None, hint=None, side=None, color_start_and_end_markers=False):
        """Add a dumbbell around a section of your life

        :param text: The text labeling the span
        :param start_date: When the era started
        :param end_date: When the era ended
        :param color: (Default value = random_color()) A matplotlib color
        :param hint: (Default value = None) Mutually exclusive with side, a Point indicating where the label should be placed. This position will be honored if possible
        :param side: (Default value = None) Mutually exclusive with hint. If Side.LEFT, the label will be on the left of the graph. Is Side.RIGHT, the label will be placed on the ride side of the graph
        :param color_start_and_end_markers: Default value = False) Colors the sqaures indicating the start and end date on the graph the same color as the text if True. The sqaures are the default color of the graph squares otherwise

        """
        if (start_date < self.birthdate or start_date > (relativedelta(years=self.ymax) + self.birthdate)):
            raise ValueError(
                f"The event date must be a valid datetime.date object that is at least as recent as the birthdate and no larger than {self.ymax}")
        if (end_date < self.birthdate or end_date > (relativedelta(years=self.ymax) + self.birthdate)):
            raise ValueError(
                f"The event date must be a valid datetime.date object that is at least as recent as the birthdate and no larger than {self.ymax}")

        if color is None:
            color = random_color()

        start_position = self.__to_date_position(start_date)
        end_position = self.__to_date_position(end_date)
        label_point = self.__get_label_point(
            hint, side, self.xmax, np.average((start_position.y, end_position.y)))

        start_marker = None
        end_marker = None
        if color_start_and_end_markers:
            start_marker = Marker(
                start_position.x, start_position.y, color=color)
            end_marker = Marker(end_position.x, end_position.y, color=color)

        # this will put a dumbbell onto the graph spanning the era
        self.era_spans.append(EraSpan(text, start_position, end_position,
                                      color, start_marker=start_marker, end_marker=end_marker))

        middle_date = start_date + (end_date - start_date)/2

        event_point = Point(np.average((start_position.x, end_position.x)), np.average(
            (start_position.y, end_position.y)))

        self.annotations.append(Annotation(middle_date, text, label_point=label_point,
                                           color=color, event_point=event_point, put_circle_around_point=False))

    def add_watermark(self, text):
        """Adds a watermark to the graph. 
        
        If this function is not called, no watermark is drawn.

        :param text: The text of the watermark

        """
        self.watermark_text = text

    def add_title(self, text, fontsize=None):
        """Adds a title to the graph.

        If this function is not called, no title is drawn.

        :param text: The text to display as the title of the graph
        :param fontsize: (Default value = None)

        """
        self.title = text
        if fontsize is not None:
            self.title_fontsize = fontsize

    def add_image(self, image_name, alpha=1):
        """Adds an image that is cliped to the axes size of the graph.

        If this function is not called, no image is drawn.

        :param image_name: param alpha:  (Default value = 1)
        :param alpha:  (Default value = 1)

        """
        self.image_name = image_name
        self.image_alpha = alpha

    def show(self):
        """Show the grpah"""
        self.__draw()
        plt.show()

    def close(self):
        """Close the graph"""
        self.fig.clf()
        plt.close()

    def save(self, name, transparent=False):
        """Save the graph.

        :param name: The name and location the file should be saved at
        :param transparent: Default value = False)

        """
        self.__draw()
        plt.savefig(name, transparent=transparent)
    #endregion Public drawing methods

    #region Private drawing methods
    def __draw(self):
        """Internal, trigger drawing of the graph"""
        plt.rcParams.update(self.settings.rcParams)

        self.fig = plt.figure()
        self.ax = self.fig.add_axes(self.axes_rect)

        xs = np.arange(1, self.xmax+1)
        ys = [np.arange(0, self.ymax) for i in range(self.xmax)]

        self.ax.plot(xs, ys)

        self.__draw_xaxis()
        self.__draw_yaxis()

        self.__draw_annotations()
        self.__draw_eras()
        self.__draw_era_spans()
        self.__draw_watermark()
        self.__draw_title()
        self.__draw_image()
        self.__draw_max_age()

        self.ax.set_aspect('equal', share=True)

    def __draw_xaxis(self):
        """Internal, draw the components of the x-axis"""
        self.ax.set_xlim(self.xlims)
        # put x ticks on top
        xticks = [1]
        xticks.extend(range(5, self.xmax+5, 5))
        fs = self.settings.rcParams["axes.labelsize"] if self.settings.otherParams[
            "xlabel.fontsize"] is None else self.settings.otherParams["xlabel.fontsize"]
        color = self.settings.rcParams["axes.labelcolor"] if self.settings.otherParams[
            "xlabel.color"] is None else self.settings.otherParams["xlabel.color"]
        self.ax.set_xticks(xticks)
        self.ax.set_xticklabels(xticks)
        self.ax.set_xlabel(self.xaxis_label, fontsize=fs, color=color)
        self.ax.xaxis.set_label_coords(
            *self.settings.otherParams["xlabel.position"])

    def __draw_yaxis(self):
        """Internal, draw the components of the y-axis"""
        self.ax.set_ylim(self.ylims)
        # set y ticks
        yticks = [*range(0, self.ymax, 5)]
        fs = self.settings.rcParams["axes.labelsize"] if self.settings.otherParams[
            "ylabel.fontsize"] is None else self.settings.otherParams["ylabel.fontsize"]
        color = self.settings.rcParams["axes.labelcolor"] if self.settings.otherParams[
            "ylabel.color"] is None else self.settings.otherParams["ylabel.color"]
        self.ax.set_yticks(yticks)
        self.ax.set_ylabel(self.yaxis_label, fontsize=fs, color=color)
        self.ax.yaxis.set_label_coords(
            *self.settings.otherParams["ylabel.position"])
        self.ax.invert_yaxis()

    def __draw_annotations(self):
        """Internal, put all of the annotations on the graph
        
        The arrowprops keyword arguments to the annotation, shrinkB, is calculated so that
        regardless of plot size, the edge of the annotaiton line ends at the edge of the circle
        """
        final = self.__resolve_annotation_conflicts(self.annotations)

        shrinkB = self.settings.rcParams["lines.markersize"]+self.settings.rcParams["lines.markeredgewidth"]
        for a in final:
            if a.put_circle_around_point:
                self.ax.plot(a.event_point.x, a.event_point.y, marker='o', markeredgecolor=a.color,
                             ms=self.settings.rcParams["lines.markersize"]*2.0)

            if a.marker is not None:
                self.ax.plot(
                    a.marker.x, a.marker.y, markeredgecolor=a.marker.color, marker=a.marker.marker)

            self.ax.annotate(a.text, xy=(a.event_point.x, a.event_point.y), xytext=(a.x, a.y),
                             weight='bold', color=a.color, va='center', ha='left',
                             arrowprops=dict(arrowstyle='-',
                                             connectionstyle='arc3',
                                             color=a.color,
                                             shrinkA=self.settings.otherParams["annotation.shrinkA"],
                                             shrinkB=shrinkB,
                                             # search for 'relpos' on https://matplotlib.org/tutorials/text/annotations.html
                                             relpos=a.relpos,
                                             linewidth=self.settings.otherParams["annotation.line.width"]))

    def __draw_eras(self):
        """Internal, draw all of the eras on the graph"""
        xmin = self.ax.transLimits.transform((1-.5, 0))[0]
        xmax = self.ax.transLimits.transform((self.xmax+.5, 0))[0]
        for era in self.eras:
            for y in range(era.start.y, era.end.y+1):
                if y == era.start.y:
                    axesUnits = self.ax.transLimits.transform(
                        (era.start.x-.5, era.start.y))
                    self.ax.axhspan(y-.5, y+.5, facecolor=era.color,
                                    alpha=era.alpha, xmin=axesUnits[0], xmax=xmax)
                elif y == era.end.y:
                    axesUnits = self.ax.transLimits.transform(
                        (era.end.x+.5, era.end.y))
                    self.ax.axhspan(y-.5, y+.5, facecolor=era.color,
                                    alpha=era.alpha, xmin=xmin, xmax=axesUnits[0])
                else:
                    self.ax.axhspan(y-.5, y+.5, facecolor=era.color,
                                    alpha=era.alpha, xmin=xmin, xmax=xmax)

    def __draw_era_spans(self):
        """Internal, draw all of the dumbbell era spans on the graph

        This is done by placing a circle around the start and end point. Then a line is drawn
        starting at the edge of each circle. The edge is found using a quadrant sensitive inverse
        tangent function and parametric equations of a circle.
        
        """
        for era in self.era_spans:
            radius = .5
            circle1 = plt.Circle((era.start.x, era.start.y), radius,
                                 color=era.color, fill=False, lw=self.settings.otherParams["annotation.edge.width"])
            circle2 = plt.Circle((era.end.x, era.end.y), radius,
                                 color=era.color, fill=False, lw=self.settings.otherParams["annotation.edge.width"])
            self.ax.add_artist(circle1)
            self.ax.add_artist(circle2)

            # to draw the line between the two circles, we need to find the point on the
            # each circle that is closest to the other circle
            # get the angle from one circle to the other and find the point on the circle
            # that lies at that angle
            x1 = era.end.x - era.start.x
            y1 = era.end.y - era.start.y

            x2 = era.start.x - era.end.x
            y2 = era.start.y - era.end.y

            # quadrant senstive arctan
            angle1 = np.arctan2(y1, x1)
            angle2 = np.arctan2(y2, x2)

            x1 = era.start.x + np.cos(angle1) * radius
            y1 = era.start.y + np.sin(angle1) * radius

            x2 = era.end.x + np.cos(angle2) * radius
            y2 = era.end.y + np.sin(angle2) * radius

            if era.start_marker is not None:
                self.ax.plot(era.start_marker.x, era.start_marker.y, color=era.start_marker.color, marker=era.start_marker.marker,
                             fillstyle=era.start_marker.fillstyle)

            if era.end_marker is not None:
                self.ax.plot(era.end_marker.x, era.end_marker.y, color=era.end_marker.color, marker=era.end_marker.marker,
                             fillstyle=era.end_marker.fillstyle)

            l = mlines.Line2D([x1, x2], [y1, y2], color=era.color, linestyle=self.settings.otherParams["era.span.linestyle"],
                              markersize=self.settings.otherParams["era.span.markersize"], linewidth=self.settings.otherParams["annotation.line.width"])
            self.ax.add_line(l)

    def __draw_watermark(self):
        """Internal, draw the watermakr"""
        if self.watermark_text is not None:
            self.fig.text(0.5, 0.5, self.watermark_text,
                          fontsize=self.settings.otherParams["watermark.fontsize"], color='gray',
                          ha='center', va='center', alpha=0.3, rotation=65, transform=self.ax.transAxes)

    def __draw_title(self):
        """Internal, draw the title"""
        if self.title is not None:
            self.fig.suptitle(
                self.title, y=self.settings.otherParams["figure.title.yposition"])

    def __draw_image(self):
        """Internal, draw the image"""
        if self.image_name is not None:
            img = mpimg.imread(self.image_name)
            extent = (0.5, self.xmax+0.5, -0.5, self.ymax-0.5)
            self.ax.imshow(img, extent=extent, origin='lower',
                           alpha=self.image_alpha)

    def __draw_max_age(self):
        if self.draw_max_age:
            self.ax.text(self.xmax+3, self.ymax, str(self.ymax),
                         fontsize=self.settings.otherParams["maxage.fontsize"],
                         ha='center', va='bottom', transform=self.ax.transData)

    def __resolve_annotation_conflicts(self, annotations):
        """Internal, Put annotation text labels on the graph while avoiding conflicts.
        
        This method decides the final (x, y) coordinates for the graph such that
        no two text label bounding boxes overlap. This happens by placing the labels
        from the top of the graph to the bottom. If any label were to overlap with
        another, it is moved down graph by the amount that it overlaps plus a buffer
        amount of space. The annotations are also sorted by their event date, so
        that labels pointing to the same line will avoid having their arcs overlap
        each other.

        :param annotations: param side:

        """
        # set the bounding box and initial positions of the annotations
        # the x-value is only corrected if it is inside the graph or too close to the graph
        left = []
        right = []
        for a in annotations:
            # first, get the bounds
            self.__set_annotation_bbox(a)

            # now set the intitial positions
            # we want all of the text to be on the left or right of the squares
            width = a.bbox.width
            # to preserve hint values, only set the x value if it is inside the graph
            # or if it is not at least as far as the offset
            if a.y >= 0 and a.y <= self.ymax:
                if ((a.x >= self.xmax / 2) and (a.x < self.xmax)) or (a.x >= self.xmax and a.x < self.xmax + self.settings.otherParams["annotation.right.offset"]):
                    a.x = self.xmax + \
                        self.settings.otherParams["annotation.right.offset"]
                elif ((a.x >= 0) and (a.x < self.xmax / 2)) or (a.x <= self.xmin and a.x > self.xmin - self.settings.otherParams["annotation.left.offset"]):
                    a.x = self.xmin - \
                        self.settings.otherParams["annotation.left.offset"] - width
                a.bbox.x0 = a.x
                a.bbox.x1 = a.x + width
                if (a.x >= self.xmax / 2):
                    a.set_relpos((0, 0.5))
                    right.append(a)
                if (a.x < self.xmax / 2):
                    a.set_relpos((1, 0.5))
                    left.append(a)
            elif a.y < 0:
                a.set_relpos((0.5, 0))
                right.append(a)
            elif a.y > self.ymax:
                a.set_relpos((0.5, 1))
                right.append(a)

        # for the left, we want to prioritze labels
        # with lower x values to minimize the crossover of annotation lines
        # for the right, we want to prioritize labels that are closer
        # to the right side of the graph to minimuze the crossover of annotation lines
        left.sort(key=lambda a: (a.event_point.y, a.event_point.x))
        right.sort(key=lambda a: (a.event_point.y, -a.event_point.x))

        final = []
        for lst in [left, right]:
            _f = []
            for unchecked in lst:
                for checked in _f:
                    if unchecked.overlaps(checked):
                        correction = unchecked.get_xy_correction(
                            checked, self.label_space_epsilon)
                        unchecked.update_Y_with_correction(correction)
                    if unchecked.is_within_epsilon_of(checked, self.label_space_epsilon):
                        correction = [0, self.label_space_epsilon]
                        unchecked.update_Y_with_correction(correction)
                _f.append(unchecked)
            final.extend(_f)

        return final

    def __to_date_position(self, date):
        """Internal, compose a DatePosition from a date

        :param date: A datetime

        """
        delta = date - self.birthdate

        year = delta.days // 365
        # Assume the start of the year for each year of your life is your birthdate
        # something that happens within or up to (not including) 7 days after the start
        # of the year happens in the first week of your life that year
        # Using this logic, your birthday will always happen on week 1 of each year
        start_of_year = self.birthdate + relativedelta(years=year)
        diff = date - start_of_year
        week = diff.days // 7

        x = week % self.xmax + 1

        return DatePosition(x, year, date)

    def __sanitize_hint(self, hint):
        """Internal, Hints should have an x value < 0 or bigger than self.xmax

        :param hint: A point or a tuple or 1x2 array

        """
        # TODO: what should this be?
        if hint is not None:
            edge = 10
            if not isinstance(hint, Point):
                hint = Point(hint[0], hint[1])
            if hint.y >= 0 and hint.y <= self.ymax:
                if (hint.x >= self.xmax / 2 and hint.x < self.xmax) or hint.x > self.xmax + edge:
                    hint.x = self.xmax
                if (hint.x > 0 and hint.x < self.xmax / 2) or hint.x < -edge:
                    hint.x = 0

        return hint

    def __set_annotation_bbox(self, a):
        """Internal, determine the bounding box of some text to aid in layout

        :param a: A string of text

        """
        # put the text on the plot temporarily so that we can determine the width of the text
        t = self.ax.text(a.x, a.y, a.text, transform=self.ax.transData,
                         ha='center', va='center')

        if (self.renderer is None):
            self.renderer = self.fig.canvas.get_renderer()

        # in display units
        bbox = t.get_window_extent(renderer=self.renderer)
        # now convert it to data units
        bbox_data_units = self.ax.transData.inverted().transform(bbox)
        a.set_bbox(Bbox(bbox_data_units))
        t.remove()

    def __get_label_point(self, hint=None, side=None, default_x=0, default_y=0, is_Era=False):
        """Internal, determine the initial position of the label using the defaults and the hint or side

        :param hint: (Default value = None) A Point, tuple, or 1x2 array
        :param side: (Default value = None) A Side
        :param default_x: (Default value = 0) Value in data coordinates
        :param default_y: (Default value = 0) Value in data coordinates
        :param is_Era: (Default value = False) Is this an era? If so, we want to set the labelx to start at 1 so that the annotation is drawn closer to the graph

        """
        if (hint is not None and side is not None):
            raise ValueError(
                f"Hint and side are mutually exclusive arguments. Specify only one of them.")
        hint = self.__sanitize_hint(hint)
        labelx = default_x
        labely = default_y

        if hint is not None:
            labelx = hint.x
            labely = hint.y

        if side is not None:
            if side == Side.LEFT:
                labelx = 0 if is_Era == False else 1
            else:
                labelx = self.xmax

        return Point(labelx, labely)
    #endregion Private drawing methods
