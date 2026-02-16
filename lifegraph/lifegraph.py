from dateutil.relativedelta import relativedelta
import datetime
import matplotlib.image as mpimg
import matplotlib.lines as mlines
from matplotlib.transforms import Bbox
import matplotlib.pyplot as plt
import numpy as np

from lifegraph.configuration import LifegraphParams, Papersize
from lifegraph.core import Point, DatePosition, Marker, Annotation, Era, EraSpan, Side
from lifegraph import serialization
from lifegraph.utils import random_color


class Lifegraph:
    """Visualize a life as a grid of weekly squares.

    Each row represents one year of life and each column one week, creating
    a 52-column by *max_age*-row grid.  Events, eras, and other annotations
    can be added and are automatically laid out to avoid overlapping labels.

    Parameters
    ----------
    birthdate : datetime.date
        The date to anchor the grid.  Row 0, column 1 corresponds to the
        first week of life.
    size : Papersize, optional
        Paper size that controls default figure dimensions and styling
        parameters.  Default is ``Papersize.A3``.
    dpi : int, optional
        Resolution in dots per inch.  Default is ``300``.
    label_space_epsilon : float, optional
        Minimum gap (in data units) the layout engine keeps between
        annotation labels.  Default is ``0.2``.
    max_age : int, optional
        Number of rows (years) in the grid.  Default is ``90``.
    axes_rect : list of float, optional
        ``[left, bottom, width, height]`` passed to
        :meth:`matplotlib.figure.Figure.add_axes`.  Ignored when *ax* is
        provided.  Default is ``[0.25, 0.1, 0.5, 0.8]``.
    ax : matplotlib.axes.Axes or None, optional
        An existing axes to draw on.  When provided, the caller is
        responsible for the figure lifecycle (saving, showing, closing).
        Default is ``None`` (a new figure is created).

    Examples
    --------
    Create a basic life graph and save it:

    >>> from lifegraph import Lifegraph
    >>> from datetime import date
    >>> g = Lifegraph(date(1990, 11, 1))
    >>> g.save("my_life.png")

    Use a provided axes for subplot composition:

    >>> import matplotlib.pyplot as plt
    >>> fig, ax = plt.subplots()
    >>> g = Lifegraph(date(1990, 11, 1), ax=ax, max_age=50)
    >>> g.draw()
    >>> fig.savefig("subplot.png")
    >>> plt.close(fig)
    """

    def __init__(self, birthdate, size=Papersize.A3, dpi=300, label_space_epsilon=0.2, max_age=90, min_age=0, axes_rect=None, ax=None):
        if birthdate is None or not isinstance(birthdate, datetime.date):
            raise ValueError("birthdate must be a valid datetime.date object")

        if min_age < 0:
            raise ValueError("min_age must be >= 0")
        if min_age >= max_age:
            raise ValueError("min_age must be less than max_age")

        self.birthdate = birthdate
        self.ax = ax  # Store the provided axes instance
        self.owns_figure = (ax is None)  # Track whether we created the figure

        self.settings = LifegraphParams(size)
        self.settings.rcParams["figure.dpi"] = dpi
        self.axes_rect = axes_rect if axes_rect is not None else [.25, .1, .5, .8]

        self.renderer = None

        # the data limits, we want a grid of 52 weeks by max_age years
        # negative minimum so that the squares are not cut off
        self.xmin = -.5
        self.xmax = 52
        self.min_age = min_age
        self.ymin = min_age - .5
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

        self.title_fontsize = None

        self._event_records = []
        self._era_records = []
        self._era_span_records = []

    #region Public drawing methods
    def format_x_axis(self, text=None, positionx=None, positiony=None, color=None, fontsize=None):
        """Customise the x-axis label appearance.

        All parameters are optional; only the supplied values are changed.

        Parameters
        ----------
        text : str or None, optional
            Replacement label text.
        positionx : float or None, optional
            X position of the label in axes coordinates.
        positiony : float or None, optional
            Y position of the label in axes coordinates.
        color : str or tuple or None, optional
            A matplotlib color.
        fontsize : float or None, optional
            Font size in points.

        Examples
        --------
        >>> g.format_x_axis(text="Weeks", color="red", fontsize=14)
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
        """Customise the y-axis label appearance.

        All parameters are optional; only the supplied values are changed.

        Parameters
        ----------
        text : str or None, optional
            Replacement label text.
        positionx : float or None, optional
            X position of the label in axes coordinates.
        positiony : float or None, optional
            Y position of the label in axes coordinates.
        color : str or tuple or None, optional
            A matplotlib color.
        fontsize : float or None, optional
            Font size in points.

        Examples
        --------
        >>> g.format_y_axis(text="Your Age", color="green")
        """
        if text is not None:
            self.yaxis_label = text

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
        """Display the maximum age number at the bottom-right of the grid.

        Examples
        --------
        >>> g = Lifegraph(date(1990, 1, 1), max_age=100)
        >>> g.show_max_age_label()
        """
        self.draw_max_age = True

    def add_life_event(self, text, date, color=None, hint=None, side=None, color_square=True):
        """Add a labeled event to the graph.

        The event position on the grid is calculated from the birthdate and
        the event *date*.  An arrow connects the label text to the
        corresponding grid square.

        Parameters
        ----------
        text : str
            Label text for the event.
        date : datetime.date
            When the event occurred.
        color : str or tuple or None, optional
            A matplotlib color.  A random color is chosen when ``None``.
        hint : Point or tuple or None, optional
            Approximate label position in data coordinates.  Mutually
            exclusive with *side*.
        side : Side or None, optional
            Force the label to :attr:`Side.LEFT` or :attr:`Side.RIGHT`.
            Mutually exclusive with *hint*.
        color_square : bool, optional
            If ``True`` (default), the grid square is colored to match the
            label.

        Raises
        ------
        ValueError
            If *date* is outside the range ``[birthdate, birthdate + max_age)``.

        Examples
        --------
        >>> from lifegraph import Lifegraph, Side
        >>> from datetime import date
        >>> g = Lifegraph(date(1990, 11, 1))
        >>> g.add_life_event("Graduated", date(2012, 5, 20), color="#00FF00")
        >>> g.add_life_event("Moved abroad", date(2015, 3, 1), side=Side.LEFT)
        """
        self.__validate_date(date)

        position = self.__to_date_position(date)

        if color is None:
            color = random_color()

        self._event_records.append({
            "text": text, "date": date, "color": color,
            "hint": hint, "side": side, "color_square": color_square,
        })

        default_x = self.xmax if (position.x >= self.xmax / 2) else 0
        label_point = self.__get_label_point(hint, side, default_x, position.y)

        marker = None
        if color_square:
            marker = Marker(position.x, position.y, color=color)

        a = Annotation(date, text, label_point=label_point, color=color,
                       event_point=Point(position.x, position.y), marker=marker,
                       source_y_range=(position.y, position.y))
        self.annotations.append(a)

    def add_era(self, text, start_date, end_date, color=None, side=None, alpha=0.3):
        """Highlight a period of your life with a colored background.

        The background spans from *start_date* to *end_date* behind the grid
        squares.

        Parameters
        ----------
        text : str
            Label text for the era.
        start_date : datetime.date
            When the era started.
        end_date : datetime.date
            When the era ended.
        color : str or tuple or None, optional
            A matplotlib color.  A random color is chosen when ``None``.
        side : Side or None, optional
            Force the label to a specific side of the grid.
        alpha : float, optional
            Opacity of the colored background.  Default is ``0.3``.

        Raises
        ------
        ValueError
            If either date is outside the valid range.

        Examples
        --------
        >>> from lifegraph import Lifegraph
        >>> from datetime import date
        >>> g = Lifegraph(date(1990, 1, 1))
        >>> g.add_era("College", date(2008, 9, 1), date(2012, 5, 15),
        ...           color="blue", alpha=0.2)
        """
        self.__validate_date(start_date)
        self.__validate_date(end_date)

        start_position = self.__to_date_position(start_date)
        end_position = self.__to_date_position(end_date)

        if color is None:
            color = random_color()

        self._era_records.append({
            "text": text, "start_date": start_date, "end_date": end_date,
            "color": color, "side": side, "alpha": alpha,
        })

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
                       event_point=label_point, put_circle_around_point=False,
                       source_y_range=(start_position.y, end_position.y))
        self.annotations.append(a)

    def add_era_span(self, text, start_date, end_date, color=None, hint=None, side=None, color_start_and_end_markers=False):
        """Add a dumbbell-shaped annotation marking a time span.

        Circles are drawn at the start and end grid positions, connected by
        a line, with a label pointing to the midpoint.

        Parameters
        ----------
        text : str
            Label text for the era span.
        start_date : datetime.date
            When the span started.
        end_date : datetime.date
            When the span ended.
        color : str or tuple or None, optional
            A matplotlib color.  A random color is chosen when ``None``.
        hint : Point or tuple or None, optional
            Approximate label position in data coordinates.  Mutually
            exclusive with *side*.
        side : Side or None, optional
            Force the label to a specific side.  Mutually exclusive with
            *hint*.
        color_start_and_end_markers : bool, optional
            If ``True``, the start and end grid squares are colored to match
            the label.  Default is ``False``.

        Raises
        ------
        ValueError
            If either date is outside the valid range.

        Examples
        --------
        >>> from lifegraph import Lifegraph
        >>> from datetime import date
        >>> g = Lifegraph(date(1990, 1, 1))
        >>> g.add_era_span("Road trip", date(2015, 6, 1),
        ...                date(2015, 8, 30), color="#D2691E")
        """
        self.__validate_date(start_date)
        self.__validate_date(end_date)

        if color is None:
            color = random_color()

        self._era_span_records.append({
            "text": text, "start_date": start_date, "end_date": end_date,
            "color": color, "hint": hint, "side": side,
            "color_start_and_end_markers": color_start_and_end_markers,
        })

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
                                           color=color, event_point=event_point, put_circle_around_point=False,
                                           source_y_range=(start_position.y, end_position.y)))

    def add_watermark(self, text):
        """Add diagonal watermark text across the graph.

        Parameters
        ----------
        text : str
            The watermark text.

        Examples
        --------
        >>> g.add_watermark("DRAFT")
        """
        self.watermark_text = text

    def add_title(self, text, fontsize=None):
        """Add a title above the graph.

        Parameters
        ----------
        text : str
            Title text.
        fontsize : float or None, optional
            Font size in points.  Uses the paper-size default when ``None``.

        Examples
        --------
        >>> g.add_title("The Life of Ada Lovelace")
        """
        self.title = text
        if fontsize is not None:
            self.title_fontsize = fontsize

    def add_image(self, image_name, alpha=1):
        """Overlay an image on the graph axes.

        The image is stretched to fill the grid area.

        Parameters
        ----------
        image_name : str
            Path to the image file.
        alpha : float, optional
            Opacity of the image overlay.  Default is ``1``.

        Examples
        --------
        >>> g.add_image("background.jpg", alpha=0.5)
        """
        self.image_name = image_name
        self.image_alpha = alpha

    def draw(self):
        """Render the graph onto the axes.

        Call this explicitly when using a provided *ax* and you want to
        trigger rendering before saving or showing the figure yourself.

        Examples
        --------
        >>> import matplotlib.pyplot as plt
        >>> fig, ax = plt.subplots()
        >>> g = Lifegraph(date(1990, 1, 1), ax=ax, max_age=50)
        >>> g.draw()
        >>> fig.savefig("out.png")
        >>> plt.close(fig)
        """
        self.__draw()

    def show(self):
        """Render the graph and display it interactively.

        When using a provided axes, the caller should call
        :func:`matplotlib.pyplot.show` on their own figure instead.

        Examples
        --------
        >>> g = Lifegraph(date(1990, 1, 1))
        >>> g.add_title("My Life")
        >>> g.show()
        """
        self.__draw()
        if self.owns_figure:
            plt.show()
        # If not owning the figure, the user should call plt.show() on their figure

    def close(self):
        """Close the figure and free resources.

        Only has an effect when the figure was created internally (i.e. no
        *ax* was provided).
        """
        if self.owns_figure and hasattr(self, 'fig'):
            self.fig.clf()
            plt.close()

    def save(self, name, transparent=False):
        """Render the graph and save it to a file.

        Parameters
        ----------
        name : str
            Output file path (e.g. ``"my_life.png"``).
        transparent : bool, optional
            Save with a transparent background.  Default is ``False``.

        Examples
        --------
        >>> g = Lifegraph(date(1990, 1, 1))
        >>> g.save("my_life.png")
        """
        self.__draw()
        # Always save the figure, regardless of ownership
        # This allows the user to call g.save() conveniently
        self.fig.savefig(name, transparent=transparent, bbox_inches='tight')

    def save_config(self, path, include_styling=False):
        """Export the graph configuration to a JSON or YAML file.

        The file format is inferred from the extension: ``.json`` for JSON,
        ``.yaml`` or ``.yml`` for YAML.

        Parameters
        ----------
        path : str or pathlib.Path
            Output file path.
        include_styling : bool, optional
            If ``True``, axis label customisations are included.
            Default is ``False``.
        """
        serialization.export_config(self, path, include_styling=include_styling)

    @classmethod
    def from_config(cls, path, apply_styling=True):
        """Create a Lifegraph from a previously exported config file.

        Parameters
        ----------
        path : str or pathlib.Path
            Path to a ``.json``, ``.yaml``, or ``.yml`` config file.
        apply_styling : bool, optional
            If ``True`` (default) and the file contains a ``styling``
            section, axis customisations are applied.

        Returns
        -------
        Lifegraph
        """
        return serialization.import_config(cls, path, apply_styling=apply_styling)
    #endregion Public drawing methods

    #region Private drawing methods
    def __draw(self):
        """Internal, trigger drawing of the graph"""
        plt.rcParams.update(self.settings.rcParams)

        # Use provided axes or create new figure and axes
        if self.ax is None:
            self.fig = plt.figure()
            self.ax = self.fig.add_axes(self.axes_rect)
        else:
            # When using provided axes, get the figure from the axes
            self.fig = self.ax.figure

        # Apply spine styling directly to axes (handles provided axes case)
        self.ax.spines[:].set_visible(False)

        xs = np.arange(1, self.xmax+1)
        ys = [np.arange(self.min_age, self.ymax) for i in range(self.xmax)]

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
        xticks.extend(range(5, self.xmax+1, 5))
        fs = self.settings.rcParams["axes.labelsize"] if self.settings.otherParams[
            "xlabel.fontsize"] is None else self.settings.otherParams["xlabel.fontsize"]
        color = self.settings.rcParams["axes.labelcolor"] if self.settings.otherParams[
            "xlabel.color"] is None else self.settings.otherParams["xlabel.color"]
        self.ax.set_xticks(xticks)
        self.ax.set_xticklabels(xticks)
        self.ax.set_xlabel(self.xaxis_label, fontsize=fs, color=color)
        self.ax.xaxis.set_label_position('top')
        if self.owns_figure:
            self.ax.xaxis.set_label_coords(
                *self.settings.otherParams["xlabel.position"])
        self.ax.tick_params(axis='x', which='major', top=False, bottom=False,
                            labeltop=True, labelbottom=False, pad=-3,
                            labelsize=self.settings.rcParams["xtick.labelsize"])
        self.ax.tick_params(axis='x', which='minor', top=False, bottom=False)

    def __draw_yaxis(self):
        """Internal, draw the components of the y-axis"""
        self.ax.set_ylim(self.ylims)
        # set y ticks
        # Start from the first multiple of 5 >= min_age
        first_tick_5 = self.min_age + (5 - self.min_age % 5) % 5
        yticks = [self.min_age] if self.min_age % 5 != 0 else []
        yticks.extend(range(first_tick_5, self.ymax, 5))
        fs = self.settings.rcParams["axes.labelsize"] if self.settings.otherParams[
            "ylabel.fontsize"] is None else self.settings.otherParams["ylabel.fontsize"]
        color = self.settings.rcParams["axes.labelcolor"] if self.settings.otherParams[
            "ylabel.color"] is None else self.settings.otherParams["ylabel.color"]
        self.ax.set_yticks(yticks)
        self.ax.set_ylabel(self.yaxis_label, fontsize=fs, color=color)
        if self.owns_figure:
            self.ax.yaxis.set_label_coords(
                *self.settings.otherParams["ylabel.position"])
        self.ax.tick_params(axis='y', which='major', left=False, right=False,
                            pad=-4,
                            labelsize=self.settings.rcParams["ytick.labelsize"])
        self.ax.tick_params(axis='y', which='minor', left=False, right=False)
        self.ax.invert_yaxis()

    def __draw_annotations(self):
        """Internal, put all of the annotations on the graph

        The arrowprops keyword arguments to the annotation, shrinkB, is calculated so that
        regardless of plot size, the edge of the annotation line ends at the edge of the circle
        """
        visible = [a for a in self.annotations if self.__is_annotation_visible(a)]
        final = self.__resolve_annotation_conflicts(visible)

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
            # skip eras entirely outside the visible range
            if era.end.y < self.min_age or era.start.y >= self.ymax:
                continue
            # clip row iteration to visible range
            row_start = max(era.start.y, self.min_age)
            row_end = min(era.end.y, self.ymax - 1)
            for y in range(row_start, row_end+1):
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
            # skip era spans entirely outside the visible range
            if era.end.y < self.min_age or era.start.y >= self.ymax:
                continue
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

            line = mlines.Line2D([x1, x2], [y1, y2], color=era.color, linestyle=self.settings.otherParams["era.span.linestyle"],
                              markersize=self.settings.otherParams["era.span.markersize"], linewidth=self.settings.otherParams["annotation.line.width"])
            self.ax.add_line(line)

    def __draw_watermark(self):
        """Internal, draw the watermakr"""
        if self.watermark_text is not None:
            self.fig.text(0.5, 0.5, self.watermark_text,
                          fontsize=self.settings.otherParams["watermark.fontsize"], color='gray',
                          ha='center', va='center', alpha=0.3, rotation=65, transform=self.ax.transAxes)

    def __draw_title(self):
        """Internal, draw the title"""
        if self.title is not None:
            self.ax.set_title(self.title)

    def __draw_image(self):
        """Internal, draw the image"""
        if self.image_name is not None:
            img = mpimg.imread(self.image_name)
            extent = (0.5, self.xmax+0.5, self.ymax-0.5, self.min_age - 0.5)
            self.ax.imshow(img, extent=extent, origin='upper',
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
            if a.y >= self.min_age and a.y <= self.ymax:
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
            elif a.y < self.min_age:
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

    def __is_annotation_visible(self, a):
        """Return True if the annotation's source overlaps [min_age, max_age)."""
        if a.source_y_range is None:
            return True
        y_lo, y_hi = a.source_y_range
        return y_hi >= self.min_age and y_lo < self.ymax

    def __validate_date(self, date):
        """Raise ValueError if *date* is outside ``[birthdate, birthdate + max_age]``."""
        max_date = self.birthdate + relativedelta(years=self.ymax)
        if date < self.birthdate or date > max_date:
            raise ValueError(
                f"The event date must be a valid datetime.date object that is at least as recent as the birthdate and no larger than {self.ymax}")

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
        if hint is not None:
            edge = 10
            if not isinstance(hint, Point):
                hint = Point(hint[0], hint[1])
            if hint.y >= self.min_age and hint.y <= self.ymax:
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
                "Hint and side are mutually exclusive arguments. Specify only one of them.")
        hint = self.__sanitize_hint(hint)
        labelx = default_x
        labely = default_y

        if hint is not None:
            labelx = hint.x
            labely = hint.y

        if side is not None:
            if side == Side.LEFT:
                labelx = 0 if not is_Era else 1
            else:
                labelx = self.xmax

        return Point(labelx, labely)
    #endregion Private drawing methods
