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

if __name__ == "__main__":
    pytest.main()