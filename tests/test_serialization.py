import datetime
import json

import pytest

from lifegraph.lifegraph import Lifegraph, Side
from lifegraph.configuration import Papersize
from lifegraph.core import Point
from lifegraph.serialization import _infer_format, CONFIG_VERSION


# ---------------------------------------------------------------------------
# Format inference
# ---------------------------------------------------------------------------

def test_infer_format_json():
    assert _infer_format("config.json") == "json"


def test_infer_format_yaml():
    assert _infer_format("config.yaml") == "yaml"
    assert _infer_format("config.yml") == "yaml"


def test_infer_format_unsupported():
    with pytest.raises(ValueError, match="Unsupported"):
        _infer_format("config.txt")


# ---------------------------------------------------------------------------
# JSON round-trip: minimal
# ---------------------------------------------------------------------------

def test_json_roundtrip_minimal(tmp_path):
    g = Lifegraph(datetime.date(1995, 11, 20), dpi=300)
    path = tmp_path / "minimal.json"
    g.save_config(str(path))

    g2 = Lifegraph.from_config(str(path))
    assert g2.birthdate == datetime.date(1995, 11, 20)
    assert g2.ymax == 90
    assert g2.settings.rcParams["figure.dpi"] == 300


# ---------------------------------------------------------------------------
# JSON round-trip: full
# ---------------------------------------------------------------------------

def test_json_roundtrip_full(tmp_path):
    g = Lifegraph(datetime.date(1995, 11, 20), dpi=300, size=Papersize.Letter,
                  label_space_epsilon=1.0, max_age=80)
    g.add_life_event("Won award", datetime.date(2013, 11, 20), "#014421",
                     hint=(25, -3), color_square=True)
    g.add_life_event("Moved", datetime.date(2015, 3, 1), "blue", side=Side.LEFT)
    g.add_era("College", datetime.date(2014, 9, 1), datetime.date(2018, 12, 14),
              (0.314, 0, 0), side=Side.LEFT, alpha=0.5)
    g.add_era_span("Vacation", datetime.date(2016, 8, 22), datetime.date(2016, 12, 16),
                   "#D2691E", hint=Point(53, 28))
    g.add_title("My Life", fontsize=24)
    g.add_watermark("DRAFT")
    g.show_max_age_label()

    path = tmp_path / "full.json"
    g.save_config(str(path))

    g2 = Lifegraph.from_config(str(path))
    assert g2.birthdate == datetime.date(1995, 11, 20)
    assert g2.ymax == 80
    assert g2.settings.size == Papersize.Letter
    assert g2.label_space_epsilon == 1.0
    assert g2.title == "My Life"
    assert g2.title_fontsize == 24
    assert g2.watermark_text == "DRAFT"
    assert g2.draw_max_age is True
    assert len(g2._event_records) == 2
    assert len(g2._era_records) == 1
    assert len(g2._era_span_records) == 1


# ---------------------------------------------------------------------------
# Color round-trip
# ---------------------------------------------------------------------------

def test_color_roundtrip(tmp_path):
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100, max_age=50)
    g.add_life_event("Hex", datetime.date(2000, 6, 1), color="#FF0000")
    g.add_life_event("Tuple", datetime.date(2001, 6, 1), color=(0.5, 0.25, 0.1))

    path = tmp_path / "colors.json"
    g.save_config(str(path))

    g2 = Lifegraph.from_config(str(path))
    assert g2._event_records[0]["color"] == "#FF0000"
    assert g2._event_records[1]["color"] == (0.5, 0.25, 0.1)


# ---------------------------------------------------------------------------
# Hint round-trip
# ---------------------------------------------------------------------------

def test_hint_roundtrip(tmp_path):
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100, max_age=50)
    g.add_life_event("With hint", datetime.date(2000, 6, 1), color="red",
                     hint=Point(25, -3))

    path = tmp_path / "hints.json"
    g.save_config(str(path))

    raw = json.loads(path.read_text())
    assert raw["events"][0]["hint"] == [25, -3]

    g2 = Lifegraph.from_config(str(path))
    hint = g2._event_records[0]["hint"]
    assert isinstance(hint, Point)
    assert hint.x == 25
    assert hint.y == -3


# ---------------------------------------------------------------------------
# Side round-trip
# ---------------------------------------------------------------------------

def test_side_roundtrip(tmp_path):
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100, max_age=50)
    g.add_life_event("Left", datetime.date(2000, 6, 1), color="red", side=Side.LEFT)
    g.add_life_event("Right", datetime.date(2001, 6, 1), color="blue", side=Side.RIGHT)

    path = tmp_path / "sides.json"
    g.save_config(str(path))

    raw = json.loads(path.read_text())
    assert raw["events"][0]["side"] == "left"
    assert raw["events"][1]["side"] == "right"

    g2 = Lifegraph.from_config(str(path))
    assert g2._event_records[0]["side"] == Side.LEFT
    assert g2._event_records[1]["side"] == Side.RIGHT


# ---------------------------------------------------------------------------
# Styling included + applied
# ---------------------------------------------------------------------------

def test_styling_included_and_applied(tmp_path):
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100)
    g.format_x_axis(text="Weeks", positionx=0.3, positiony=1.1, color="red", fontsize=14)
    g.format_y_axis(text="Age", positionx=-0.05, positiony=0.9, color="green", fontsize=16)

    path = tmp_path / "styled.json"
    g.save_config(str(path), include_styling=True)

    g2 = Lifegraph.from_config(str(path))
    assert g2.xaxis_label == "Weeks"
    assert g2.settings.otherParams["xlabel.position"] == (0.3, 1.1)
    assert g2.settings.otherParams["xlabel.color"] == "red"
    assert g2.settings.otherParams["xlabel.fontsize"] == 14
    assert g2.yaxis_label == "Age"
    assert g2.settings.otherParams["ylabel.position"] == (-0.05, 0.9)
    assert g2.settings.otherParams["ylabel.color"] == "green"
    assert g2.settings.otherParams["ylabel.fontsize"] == 16


# ---------------------------------------------------------------------------
# Styling included + NOT applied
# ---------------------------------------------------------------------------

def test_styling_not_applied(tmp_path):
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100)
    g.format_x_axis(text="Weeks")

    path = tmp_path / "styled2.json"
    g.save_config(str(path), include_styling=True)

    g2 = Lifegraph.from_config(str(path), apply_styling=False)
    # Default x-axis label, not the custom one
    assert g2.xaxis_label == r'Week of the Year $\longrightarrow$'


# ---------------------------------------------------------------------------
# Styling not included
# ---------------------------------------------------------------------------

def test_styling_not_included(tmp_path):
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100)
    g.format_x_axis(text="Weeks")

    path = tmp_path / "no_style.json"
    g.save_config(str(path), include_styling=False)

    raw = json.loads(path.read_text())
    assert "styling" not in raw


# ---------------------------------------------------------------------------
# YAML round-trip
# ---------------------------------------------------------------------------

def test_yaml_roundtrip(tmp_path):
    pytest.importorskip("yaml")

    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100, max_age=50)
    g.add_life_event("Test", datetime.date(2000, 6, 1), color="red")

    for ext in (".yaml", ".yml"):
        path = tmp_path / f"config{ext}"
        g.save_config(str(path))

        g2 = Lifegraph.from_config(str(path))
        assert g2.birthdate == datetime.date(1990, 1, 1)
        assert len(g2._event_records) == 1


# ---------------------------------------------------------------------------
# Defaults omitted
# ---------------------------------------------------------------------------

def test_defaults_omitted(tmp_path):
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=300, max_age=90)
    g.add_life_event("Ev", datetime.date(2000, 6, 1), color="red", color_square=True)
    g.add_era("Era", datetime.date(2000, 1, 1), datetime.date(2005, 1, 1),
              color="blue", alpha=0.3)

    path = tmp_path / "defaults.json"
    g.save_config(str(path))

    raw = json.loads(path.read_text())

    # Constructor defaults omitted
    assert "max_age" not in raw
    assert "dpi" not in raw
    assert "size" not in raw

    # color_square=True (default) omitted
    assert "color_square" not in raw["events"][0]

    # alpha=0.3 (default) omitted
    assert "alpha" not in raw["eras"][0]


# ---------------------------------------------------------------------------
# Title as bare string
# ---------------------------------------------------------------------------

def test_title_bare_string(tmp_path):
    path = tmp_path / "bare_title.json"
    path.write_text(json.dumps({
        "version": CONFIG_VERSION,
        "birthdate": "1990-01-01",
        "title": "Hello World"
    }))

    g = Lifegraph.from_config(str(path))
    assert g.title == "Hello World"
    assert g.title_fontsize is None


# ---------------------------------------------------------------------------
# Unsupported extension error
# ---------------------------------------------------------------------------

def test_save_config_unsupported_ext(tmp_path):
    g = Lifegraph(datetime.date(1990, 1, 1), dpi=100)
    with pytest.raises(ValueError, match="Unsupported"):
        g.save_config(str(tmp_path / "bad.txt"))


def test_from_config_unsupported_ext(tmp_path):
    with pytest.raises(ValueError, match="Unsupported"):
        Lifegraph.from_config(str(tmp_path / "bad.txt"))


# ---------------------------------------------------------------------------
# Unsupported version error
# ---------------------------------------------------------------------------

def test_unsupported_version(tmp_path):
    path = tmp_path / "bad_version.json"
    path.write_text(json.dumps({
        "version": 99,
        "birthdate": "1990-01-01"
    }))

    with pytest.raises(ValueError, match="Unsupported config version"):
        Lifegraph.from_config(str(path))


# ---------------------------------------------------------------------------
# Render after import
# ---------------------------------------------------------------------------

def test_render_after_import(tmp_path):
    g = Lifegraph(datetime.date(1995, 11, 20), dpi=100, size=Papersize.Letter, max_age=50)
    g.add_life_event("Won award", datetime.date(2013, 11, 20), "#014421")
    g.add_era("College", datetime.date(2014, 9, 1), datetime.date(2018, 12, 14), "blue")
    g.add_era_span("Vacation", datetime.date(2016, 8, 22), datetime.date(2016, 12, 16), "#D2691E")
    g.add_title("Test")

    config_path = tmp_path / "render.json"
    g.save_config(str(config_path))

    g2 = Lifegraph.from_config(str(config_path))
    img_path = tmp_path / "render.png"
    g2.save(str(img_path))

    assert img_path.exists()
    assert img_path.stat().st_size > 0
    g2.close()
