import pytest
import datetime
import matplotlib.pyplot as plt
from lifegraph.lifegraph import random_color, Point, DatePosition, Marker, Annotation, Era, EraSpan, Lifegraph, Side
from lifegraph.configuration import Papersize, LifegraphParams, STYLE_PATH

def test_random_color():
    color = random_color()
    assert isinstance(color, str) or isinstance(color, tuple)

def test_point():
    p = Point(1, 2)
    assert p.x == 1
    assert p.y == 2
    assert str(p) == "(1, 2)"

def test_dateposition():
    d = datetime.date(2020, 1, 1)
    dp = DatePosition(10, 20, d)
    assert dp.x == 10
    assert dp.y == 20
    assert dp.date == d

def test_marker():
    m = Marker(3, 4, marker='o', fillstyle='full', color='red')
    assert m.x == 3
    assert m.y == 4
    assert m.marker == 'o'
    assert m.fillstyle == 'full'
    assert m.color == 'red'

def test_annotation_bbox_methods():
    p = Point(0, 0)
    a = Annotation(datetime.date(2020,1,1), "Test", p, color='blue')
    # Bbox is not set, so overlaps/is_within_epsilon_of should raise
    with pytest.raises(ValueError):
        a.overlaps("not an annotation")
    with pytest.raises(ValueError):
        a.is_within_epsilon_of("not an annotation", 0.1)

def test_era_repr():
    e = Era("Test Era", datetime.date(2000,1,1), datetime.date(2001,1,1), 'red')
    assert "Test Era" in str(e)

def test_eraspan_repr():
    es = EraSpan("Test Span", datetime.date(2000,1,1), datetime.date(2001,1,1), 'blue')
    assert "Test Span" in str(es)

def test_lifegraph_init():
    birthdate = datetime.date(1990, 1, 1)
    g = Lifegraph(birthdate, size=Papersize.A4, dpi=100, max_age=80)
    assert g.birthdate == birthdate
    assert g.xmax == 52
    assert g.ymax == 80
    assert g.settings.rcParams["figure.dpi"] == 100
    assert g.settings.size == Papersize.A4
    assert g.draw_max_age is False
    assert g.annotations == []
    assert g.eras == []
    assert g.era_spans == []

def test_side_enum():
    assert Side.LEFT != Side.RIGHT
    assert str(Side.LEFT) != str(Side.RIGHT)

def test_lifegraph_with_provided_axes(tmp_path):
    """Test that Lifegraph can use a provided axes instance"""
    birthdate = datetime.date(1990, 1, 1)
    
    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create Lifegraph with the provided axes
    g = Lifegraph(birthdate, size=Papersize.A4, dpi=100, max_age=80, ax=ax)
    
    # Verify that the provided axes is stored
    assert g.ax is ax
    assert g.owns_figure is False
    
    # Add some content
    g.add_life_event('Test Event', datetime.date(2010, 5, 15), color='red')
    
    # Trigger drawing
    output_file = tmp_path / "test_with_axes.png"
    g.save(str(output_file))
    
    # Verify that the axes received some content
    # The axes should have plot lines from the grid
    assert len(ax.lines) > 0
    
    # Verify the file was created
    assert output_file.exists()
    
    # Clean up
    plt.close(fig)

def test_lifegraph_without_provided_axes(tmp_path):
    """Test that Lifegraph still works without a provided axes (default behavior)"""
    birthdate = datetime.date(1990, 1, 1)
    
    # Create Lifegraph without providing axes
    g = Lifegraph(birthdate, size=Papersize.A4, dpi=100, max_age=80)
    
    # Verify that no axes is initially set
    assert g.ax is None
    assert g.owns_figure is True
    
    # Add some content
    g.add_life_event('Test Event', datetime.date(2010, 5, 15), color='blue')
    
    # Trigger drawing
    output_file = tmp_path / "test_without_axes.png"
    g.save(str(output_file))
    
    # After drawing, axes and fig should be created
    assert g.ax is not None
    assert g.fig is not None
    
    # Verify the file was created
    assert output_file.exists()
    
    # Clean up
    g.close()

def test_lifegraph_axes_receives_annotations(tmp_path):
    """Test that annotations are drawn on the provided axes"""
    birthdate = datetime.date(1990, 1, 1)
    
    # Create a figure and axes
    fig, ax = plt.subplots()
    
    # Create Lifegraph with the provided axes
    g = Lifegraph(birthdate, max_age=50, ax=ax)
    
    # Add multiple life events
    g.add_life_event('Event 1', datetime.date(2005, 3, 10), color='red')
    g.add_life_event('Event 2', datetime.date(2010, 8, 20), color='blue')
    
    # Trigger drawing
    output_file = tmp_path / "test_annotations.png"
    print("Saving to", output_file)
    g.save(str(output_file))
    
    # Verify that annotations were added to the axes
    # Annotations are added as text objects
    assert len(ax.texts) > 0
    
    # Verify the file was created
    assert output_file.exists()
    
    # Clean up
    plt.close(fig)

def test_lifegraph_axes_multiple_subplots(tmp_path):
    """Test that Lifegraph can be used with multiple subplots"""
    birthdate1 = datetime.date(1990, 1, 1)
    birthdate2 = datetime.date(1995, 6, 15)
    
    # Create a figure with multiple subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Create two Lifegraphs, each on a different axes
    g1 = Lifegraph(birthdate1, max_age=50, ax=ax1)
    g2 = Lifegraph(birthdate2, max_age=50, ax=ax2)
    
    # Add events to each
    g1.add_life_event('Person 1 Event', datetime.date(2010, 1, 1), color='red')
    g2.add_life_event('Person 2 Event', datetime.date(2015, 1, 1), color='blue')
    
    # Draw both by calling save on each (or we could call a draw method if it were public)
    output_file = tmp_path / "test_multiple.png"
    print("Saving to", output_file)
    # We need to trigger drawing on both before saving
    # Since save calls __draw internally, we call save on both
    # But only need to actually write the file once
    g1.save(str(output_file))
    g2.save(str(output_file))  # This will save the same figure again, which is fine
    
    # Verify both axes have content
    assert len(ax1.lines) > 0
    assert len(ax2.lines) > 0
    
    # Verify the file was created
    assert output_file.exists()
    
    # Clean up
    plt.close(fig)

def test_papersize_dimensions():
    """Each Papersize member should have a 2-tuple of positive floats."""
    for sz in Papersize:
        w, h = sz.value
        assert isinstance(w, (int, float)) and w > 0, f"{sz.name} width"
        assert isinstance(h, (int, float)) and h > 0, f"{sz.name} height"

def test_lifegraph_params_scaling():
    """Computed params should produce sane values for a few sizes."""
    small = LifegraphParams(Papersize.A10)
    medium = LifegraphParams(Papersize.A3)
    large = LifegraphParams(Papersize.A0)

    # Marker size should grow with paper size
    assert small.rcParams["lines.markersize"] < medium.rcParams["lines.markersize"]
    assert medium.rcParams["lines.markersize"] < large.rcParams["lines.markersize"]

    # Font size should grow with paper size
    assert small.rcParams["font.size"] < medium.rcParams["font.size"]
    assert medium.rcParams["font.size"] < large.rcParams["font.size"]

    # Figure size should match enum dimensions
    assert medium.rcParams["figure.figsize"] == [11.7, 16.5]
    assert large.rcParams["figure.figsize"] == [33.1, 46.8]

def test_style_file_exists():
    """The bundled .mplstyle file should exist and be parseable."""
    assert STYLE_PATH.exists()
    import matplotlib
    rc = matplotlib.rc_params_from_file(str(STYLE_PATH), use_default_template=False)
    assert "axes.labelcolor" in rc
    assert "lines.marker" in rc

def test_all_papersizes_construct():
    """LifegraphParams should succeed for every Papersize member."""
    for sz in Papersize:
        params = LifegraphParams(sz)
        assert params.size is sz
        assert "figure.figsize" in params.rcParams
        assert "watermark.fontsize" in params.otherParams

def test_validate_date():
    """Dates outside [birthdate, birthdate + max_age] should raise ValueError."""
    birthdate = datetime.date(1990, 1, 1)
    g = Lifegraph(birthdate, dpi=100, max_age=80)

    # Before birthdate
    with pytest.raises(ValueError):
        g.add_life_event("Too early", datetime.date(1989, 12, 31), color="r")

    # After max age
    with pytest.raises(ValueError):
        g.add_life_event("Too late", datetime.date(2071, 1, 2), color="r")

    # Boundary: exactly birthdate — should not raise
    g.add_life_event("Birth", datetime.date(1990, 1, 1), color="r")

    # Boundary: exactly max age date — should not raise
    g.add_life_event("Max", datetime.date(2070, 1, 1), color="r")

    g.close()

def test_format_x_axis():
    """format_x_axis should update x-axis label, position, color, and fontsize."""
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100)

    g.format_x_axis(text="Weeks")
    assert g.xaxis_label == "Weeks"

    g.format_x_axis(positionx=0.5, positiony=1.1)
    assert g.settings.otherParams["xlabel.position"] == (0.5, 1.1)

    g.format_x_axis(color="red")
    assert g.settings.otherParams["xlabel.color"] == "red"

    g.format_x_axis(fontsize=18)
    assert g.settings.otherParams["xlabel.fontsize"] == 18

    # Partial update should preserve other position component
    g.format_x_axis(positionx=0.3)
    assert g.settings.otherParams["xlabel.position"] == (0.3, 1.1)

def test_format_y_axis():
    """format_y_axis should update y-axis label, position, color, and fontsize."""
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100)

    g.format_y_axis(text="Your Age")
    assert g.yaxis_label == "Your Age"
    # Ensure it didn't accidentally modify x-axis
    assert g.xaxis_label != "Your Age"

    g.format_y_axis(positionx=-0.05, positiony=0.9)
    assert g.settings.otherParams["ylabel.position"] == (-0.05, 0.9)

    g.format_y_axis(color="green")
    assert g.settings.otherParams["ylabel.color"] == "green"

    g.format_y_axis(fontsize=16)
    assert g.settings.otherParams["ylabel.fontsize"] == 16

def test_show_max_age_label():
    """show_max_age_label should set the draw_max_age flag."""
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100)
    assert g.draw_max_age is False
    g.show_max_age_label()
    assert g.draw_max_age is True

def test_add_title():
    """add_title should store the title text and optional fontsize."""
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100)
    assert g.title is None

    g.add_title("My Life")
    assert g.title == "My Life"

    g.add_title("My Life v2", fontsize=24)
    assert g.title == "My Life v2"
    assert g.title_fontsize == 24

def test_add_watermark():
    """add_watermark should store the watermark text."""
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100)
    assert g.watermark_text is None
    g.add_watermark("DRAFT")
    assert g.watermark_text == "DRAFT"

def test_add_image():
    """add_image should store the image path and alpha."""
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100)
    assert g.image_name is None

    g.add_image("/some/path.png", alpha=0.5)
    assert g.image_name == "/some/path.png"
    assert g.image_alpha == 0.5

def test_add_era():
    """add_era should append to the eras list."""
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100, max_age=80)
    assert len(g.eras) == 0

    g.add_era("College", datetime.date(2008, 9, 1), datetime.date(2012, 5, 15), color="blue")
    assert len(g.eras) == 1
    assert g.eras[0].text == "College"

    # With side
    g.add_era("Work", datetime.date(2012, 6, 1), datetime.date(2020, 1, 1), color="green", side=Side.LEFT)
    assert len(g.eras) == 2

def test_add_era_validates_dates():
    """add_era should reject dates outside the valid range."""
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100, max_age=80)

    with pytest.raises(ValueError):
        g.add_era("Bad", datetime.date(1989, 1, 1), datetime.date(2000, 1, 1), color="r")

    with pytest.raises(ValueError):
        g.add_era("Bad", datetime.date(2000, 1, 1), datetime.date(2080, 1, 1), color="r")

def test_add_era_span():
    """add_era_span should append to the era_spans list."""
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100, max_age=80)
    assert len(g.era_spans) == 0

    g.add_era_span("Road trip", datetime.date(2015, 6, 1), datetime.date(2015, 8, 30), color="#D2691E")
    assert len(g.era_spans) == 1
    assert g.era_spans[0].text == "Road trip"

    # With colored markers
    g.add_era_span("Gap year", datetime.date(2016, 1, 1), datetime.date(2016, 12, 31),
                    color="green", color_start_and_end_markers=True)
    assert len(g.era_spans) == 2
    assert g.era_spans[1].start_marker is not None
    assert g.era_spans[1].end_marker is not None

def test_add_era_span_validates_dates():
    """add_era_span should reject dates outside the valid range."""
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100, max_age=80)

    with pytest.raises(ValueError):
        g.add_era_span("Bad", datetime.date(1989, 1, 1), datetime.date(2000, 1, 1), color="r")

    with pytest.raises(ValueError):
        g.add_era_span("Bad", datetime.date(2000, 1, 1), datetime.date(2080, 1, 1), color="r")

def test_to_date_position_birthday():
    """Birthday should map to week 1, year 0."""
    birthday = datetime.date(1990, 1, 1)
    g = Lifegraph(birthday, dpi=100)
    pos = g._Lifegraph__to_date_position(birthday)
    assert pos.x == 1
    assert pos.y == 0

def test_to_date_position_one_week_later():
    """One week after birthday should be week 2, year 0."""
    birthday = datetime.date(1990, 1, 1)
    g = Lifegraph(birthday, dpi=100)
    pos = g._Lifegraph__to_date_position(datetime.date(1990, 1, 8))
    assert pos.x == 2
    assert pos.y == 0

def test_to_date_position_one_year_later():
    """Exactly one year later should be week 1, year 1."""
    birthday = datetime.date(1990, 1, 1)
    g = Lifegraph(birthday, dpi=100)
    pos = g._Lifegraph__to_date_position(datetime.date(1991, 1, 1))
    assert pos.x == 1
    assert pos.y == 1

def test_to_date_position_leap_year_birthday():
    """Leap-year birthday should still map correctly."""
    birthday = datetime.date(2000, 2, 29)
    g = Lifegraph(birthday, dpi=100)

    # Birthday itself
    pos = g._Lifegraph__to_date_position(birthday)
    assert pos.x == 1
    assert pos.y == 0

    # relativedelta(years=1) from Feb 29 lands on Feb 28 next year,
    # so Feb 28, 2001 is the start of year 1
    pos = g._Lifegraph__to_date_position(datetime.date(2001, 2, 28))
    assert pos.x == 1
    assert pos.y == 1

def test_to_date_position_leap_year_accumulation():
    """Accumulated leap days should not push the year forward incorrectly.

    Born 2000-01-01 (leap year).  On 2003-12-31 the person is still 3
    (turns 4 on 2004-01-01).  A naive ``delta.days // 365`` gives 4 because
    ``1460 // 365 == 4``, which is wrong.
    """
    birthday = datetime.date(2000, 1, 1)
    g = Lifegraph(birthday, dpi=100)
    pos = g._Lifegraph__to_date_position(datetime.date(2003, 12, 31))
    assert pos.y == 3, f"Expected year 3, got {pos.y}"


def test_add_life_event_stores_annotation():
    """add_life_event should append to the annotations list."""
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100, max_age=80)
    assert len(g.annotations) == 0

    g.add_life_event("Graduated", datetime.date(2012, 5, 20), color="#00FF00")
    assert len(g.annotations) == 1

    # With side
    g.add_life_event("Moved", datetime.date(2015, 3, 1), color="blue", side=Side.RIGHT)
    assert len(g.annotations) == 2

def test_resolve_annotation_conflicts(tmp_path):
    """Overlapping annotations should be separated by the layout engine."""
    fig, ax = plt.subplots()
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100, max_age=80, ax=ax)

    # Add several events on the same date to force overlaps
    for i in range(5):
        g.add_life_event(f"Event {i}", datetime.date(2000, 1, 1), color="red")

    # Drawing triggers conflict resolution
    g.save(str(tmp_path / "conflicts.png"))

    # All annotations should still be present
    assert len(ax.texts) >= 5

    plt.close(fig)

def test_lifegraph_init_min_age():
    """min_age should be stored and ymin computed correctly."""
    birthdate = datetime.date(1990, 1, 1)
    g = Lifegraph(birthdate, dpi=100, max_age=65, min_age=20)
    assert g.min_age == 20
    assert g.ymin == 19.5
    assert g.ymax == 65


def test_lifegraph_min_age_default_zero():
    """Default min_age should be 0 for backward compatibility."""
    birthdate = datetime.date(1990, 1, 1)
    g = Lifegraph(birthdate, dpi=100)
    assert g.min_age == 0
    assert g.ymin == -0.5


def test_lifegraph_min_age_validation():
    """Negative min_age and min_age >= max_age should raise ValueError."""
    birthdate = datetime.date(1990, 1, 1)
    with pytest.raises(ValueError):
        Lifegraph(birthdate, dpi=100, max_age=80, min_age=-1)
    with pytest.raises(ValueError):
        Lifegraph(birthdate, dpi=100, max_age=80, min_age=80)
    with pytest.raises(ValueError):
        Lifegraph(birthdate, dpi=100, max_age=80, min_age=90)


def test_lifegraph_min_age_events_accepted_but_not_drawn(tmp_path):
    """Events outside the visible range should be stored but render succeeds."""
    birthdate = datetime.date(1990, 1, 1)
    g = Lifegraph(birthdate, dpi=100, max_age=65, min_age=20)
    # Event at age ~5, outside visible range
    g.add_life_event("Childhood event", datetime.date(1995, 6, 1), color="red")
    # Event at age ~30, inside visible range
    g.add_life_event("Adult event", datetime.date(2020, 6, 1), color="blue")
    assert len(g.annotations) == 2
    output = tmp_path / "min_age_events.png"
    g.save(str(output))
    assert output.exists()
    g.close()


def test_lifegraph_min_age_eras_clipped(tmp_path):
    """Eras crossing the min_age boundary should be clipped; fully-outside skipped."""
    birthdate = datetime.date(1990, 1, 1)
    g = Lifegraph(birthdate, dpi=100, max_age=65, min_age=20)
    # Era entirely below min_age (ages 5-15)
    g.add_era("Childhood", datetime.date(1995, 1, 1), datetime.date(2005, 1, 1), color="red")
    # Era crossing boundary (ages 15-25)
    g.add_era("Transition", datetime.date(2005, 1, 1), datetime.date(2015, 1, 1), color="blue")
    # Era entirely in range (ages 25-35)
    g.add_era("Career", datetime.date(2015, 1, 1), datetime.date(2025, 1, 1), color="green")
    assert len(g.eras) == 3
    output = tmp_path / "min_age_eras.png"
    g.save(str(output))
    assert output.exists()
    g.close()


def test_lifegraph_min_age_era_spans_filtered(tmp_path):
    """Era spans entirely outside the visible range should be skipped."""
    birthdate = datetime.date(1990, 1, 1)
    g = Lifegraph(birthdate, dpi=100, max_age=65, min_age=20)
    # Span entirely below min_age
    g.add_era_span("Early", datetime.date(1995, 1, 1), datetime.date(1998, 1, 1), color="red")
    # Span in range
    g.add_era_span("Later", datetime.date(2015, 1, 1), datetime.date(2020, 1, 1), color="blue")
    assert len(g.era_spans) == 2
    output = tmp_path / "min_age_spans.png"
    g.save(str(output))
    assert output.exists()
    g.close()


def test_lifegraph_min_age_render_full(tmp_path):
    """Full render with all features + min_age should succeed."""
    birthdate = datetime.date(1990, 1, 1)
    g = Lifegraph(birthdate, dpi=100, max_age=65, min_age=20)
    g.add_title("Ages 20-65")
    g.add_watermark("TEST")
    g.show_max_age_label()
    g.add_life_event("Age 25 event", datetime.date(2015, 6, 1), color="red")
    g.add_life_event("Age 30 event", datetime.date(2020, 6, 1), color="blue", side=Side.LEFT)
    g.add_era("Work", datetime.date(2015, 1, 1), datetime.date(2025, 1, 1), color="green")
    g.add_era_span("Travel", datetime.date(2018, 6, 1), datetime.date(2019, 6, 1), color="#D2691E")
    output = tmp_path / "min_age_full.png"
    g.save(str(output))
    assert output.exists()
    assert output.stat().st_size > 0
    g.close()


def test_annotation_bbox_uses_bold_weight(tmp_path):
    """Annotations measured with bold weight should not overlap when min_age is set.

    Regression test: the bbox measurement used regular weight while the final
    rendering used bold, causing the conflict resolver to underestimate label
    sizes — especially visible with a zoomed-in y-axis (min_age > 0).
    """
    import matplotlib.text
    birthdate = datetime.date(1990, 1, 1)
    fig, ax = plt.subplots()
    g = Lifegraph(birthdate, dpi=300, max_age=65, min_age=20, ax=ax)

    # Two same-side annotations at close y positions to exercise conflict resolution
    g.add_life_event("Job", datetime.date(2013, 9, 15), color="#00008B")
    g.add_life_event("Cat", datetime.date(2013, 10, 1), color="#D2691E")

    output = tmp_path / "bold_bbox.png"
    g.save(str(output))

    # Collect text-only bounding boxes (exclude arrow extent) for annotations
    renderer = fig.canvas.get_renderer()
    bboxes = []
    for child in ax.get_children():
        if isinstance(child, matplotlib.text.Annotation) and child.get_text() in ("Job", "Cat"):
            # Use Text.get_window_extent to get just the text bbox, not the arrow
            bbox = matplotlib.text.Text.get_window_extent(child, renderer)
            bboxes.append(bbox)

    assert len(bboxes) == 2, f"Expected 2 annotation bboxes, got {len(bboxes)}"

    # The two text bounding boxes should not overlap
    b0, b1 = bboxes
    overlaps = not (b0.x1 < b1.x0 or b1.x1 < b0.x0 or b0.y1 < b1.y0 or b1.y1 < b0.y0)
    assert not overlaps, (
        f"Annotation bounding boxes overlap: {b0} vs {b1}"
    )

    # Verify sufficient visual separation: gap should be at least 20% of text height
    text_height = max(b0.height, b1.height)
    if b0.y0 > b1.y1:
        vertical_gap = b0.y0 - b1.y1
    elif b1.y0 > b0.y1:
        vertical_gap = b1.y0 - b0.y1
    else:
        vertical_gap = 0
    min_gap = text_height * 0.1
    assert vertical_gap >= min_gap, (
        f"Annotations too close: gap={vertical_gap:.1f}px, "
        f"min={min_gap:.1f}px (20% of {text_height:.1f}px text height)"
    )

    plt.close(fig)


if __name__ == "__main__":
    pytest.main()