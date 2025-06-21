import pytest
import datetime
from lifegraph.lifegraph import random_color, Point, DatePosition, Marker, Annotation, Era, EraSpan, Lifegraph, Side
from lifegraph.configuration import Papersize

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
