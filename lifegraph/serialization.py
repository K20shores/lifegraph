import datetime
import json
from pathlib import Path

from lifegraph.configuration import Papersize
from lifegraph.core import Point, Side


CONFIG_VERSION = 1


def _infer_format(path):
    ext = Path(path).suffix.lower()
    if ext == ".json":
        return "json"
    if ext in (".yaml", ".yml"):
        return "yaml"
    raise ValueError(f"Unsupported config file extension '{ext}'. Use .json, .yaml, or .yml.")


def _get_yaml():
    try:
        import yaml
        return yaml
    except ImportError:
        raise ImportError(
            "PyYAML is required for YAML support. Install it with: pip install pyyaml"
        ) from None


# ---------------------------------------------------------------------------
# Serialization helpers
# ---------------------------------------------------------------------------

def _serialize_date(d):
    return d.isoformat()


def _serialize_color(c):
    if isinstance(c, tuple):
        return list(c)
    return c


def _serialize_hint(h):
    if h is None:
        return None
    if isinstance(h, Point):
        return [h.x, h.y]
    if isinstance(h, (list, tuple)):
        return [h[0], h[1]]
    return None


def _serialize_side(s):
    if s is None:
        return None
    if isinstance(s, Side):
        return s.name.lower()
    return s


def _build_config_dict(graph, include_styling):
    d = {
        "version": CONFIG_VERSION,
        "birthdate": _serialize_date(graph.birthdate),
    }

    if graph.ymax != 90:
        d["max_age"] = graph.ymax

    if graph.settings.size != Papersize.A3:
        d["size"] = graph.settings.size.name

    if graph.settings.rcParams["figure.dpi"] != 300:
        d["dpi"] = graph.settings.rcParams["figure.dpi"]

    if graph.label_space_epsilon != 0.2:
        d["label_space_epsilon"] = graph.label_space_epsilon

    if graph.title is not None:
        if graph.title_fontsize is not None:
            d["title"] = {"text": graph.title, "fontsize": graph.title_fontsize}
        else:
            d["title"] = graph.title

    if graph.watermark_text is not None:
        d["watermark"] = graph.watermark_text

    if graph.image_name is not None:
        img = {"path": graph.image_name}
        if graph.image_alpha != 1:
            img["alpha"] = graph.image_alpha
        d["image"] = img

    if graph.draw_max_age:
        d["show_max_age_label"] = True

    if graph._event_records:
        events = []
        for rec in graph._event_records:
            ev = {
                "text": rec["text"],
                "date": _serialize_date(rec["date"]),
                "color": _serialize_color(rec["color"]),
            }
            hint = _serialize_hint(rec.get("hint"))
            if hint is not None:
                ev["hint"] = hint
            side = _serialize_side(rec.get("side"))
            if side is not None:
                ev["side"] = side
            if not rec.get("color_square", True):
                ev["color_square"] = False
            events.append(ev)
        d["events"] = events

    if graph._era_records:
        eras = []
        for rec in graph._era_records:
            era = {
                "text": rec["text"],
                "start_date": _serialize_date(rec["start_date"]),
                "end_date": _serialize_date(rec["end_date"]),
                "color": _serialize_color(rec["color"]),
            }
            side = _serialize_side(rec.get("side"))
            if side is not None:
                era["side"] = side
            if rec.get("alpha") != 0.3:
                era["alpha"] = rec["alpha"]
            eras.append(era)
        d["eras"] = eras

    if graph._era_span_records:
        spans = []
        for rec in graph._era_span_records:
            span = {
                "text": rec["text"],
                "start_date": _serialize_date(rec["start_date"]),
                "end_date": _serialize_date(rec["end_date"]),
                "color": _serialize_color(rec["color"]),
            }
            hint = _serialize_hint(rec.get("hint"))
            if hint is not None:
                span["hint"] = hint
            side = _serialize_side(rec.get("side"))
            if side is not None:
                span["side"] = side
            if rec.get("color_start_and_end_markers"):
                span["color_start_and_end_markers"] = True
            spans.append(span)
        d["era_spans"] = spans

    if include_styling:
        styling = {}

        x_ax = {}
        if graph.xaxis_label != r'Week of the Year $\longrightarrow$':
            x_ax["text"] = graph.xaxis_label
        x_pos = graph.settings.otherParams["xlabel.position"]
        if x_pos != (0.20, 1.05):
            x_ax["positionx"] = x_pos[0]
            x_ax["positiony"] = x_pos[1]
        if graph.settings.otherParams["xlabel.color"] is not None:
            x_ax["color"] = _serialize_color(graph.settings.otherParams["xlabel.color"])
        if graph.settings.otherParams["xlabel.fontsize"] is not None:
            x_ax["fontsize"] = graph.settings.otherParams["xlabel.fontsize"]
        if x_ax:
            styling["x_axis"] = x_ax

        y_ax = {}
        if graph.yaxis_label != r'$\longleftarrow$ Age':
            y_ax["text"] = graph.yaxis_label
        y_pos = graph.settings.otherParams["ylabel.position"]
        if y_pos != (-0.03, 0.95):
            y_ax["positionx"] = y_pos[0]
            y_ax["positiony"] = y_pos[1]
        if graph.settings.otherParams["ylabel.color"] is not None:
            y_ax["color"] = _serialize_color(graph.settings.otherParams["ylabel.color"])
        if graph.settings.otherParams["ylabel.fontsize"] is not None:
            y_ax["fontsize"] = graph.settings.otherParams["ylabel.fontsize"]
        if y_ax:
            styling["y_axis"] = y_ax

        if styling:
            d["styling"] = styling

    return d


def export_config(graph, path, include_styling=False):
    fmt = _infer_format(path)
    d = _build_config_dict(graph, include_styling)

    with open(path, "w") as f:
        if fmt == "json":
            json.dump(d, f, indent=2)
        else:
            yaml = _get_yaml()
            yaml.dump(d, f, default_flow_style=False, sort_keys=False)


# ---------------------------------------------------------------------------
# Deserialization helpers
# ---------------------------------------------------------------------------

def _parse_date(s):
    return datetime.date.fromisoformat(s)


def _parse_color(c):
    if isinstance(c, list):
        return tuple(c)
    return c


def _parse_hint(h):
    if h is None:
        return None
    if isinstance(h, list):
        return Point(h[0], h[1])
    return h


def _parse_side(s):
    if s is None:
        return None
    if isinstance(s, str):
        return Side[s.upper()]
    return s


def _parse_papersize(s):
    if s is None:
        return Papersize.A3
    if isinstance(s, str):
        return Papersize[s]
    return s


def import_config(cls, path, apply_styling=True):
    fmt = _infer_format(path)

    with open(path) as f:
        if fmt == "json":
            d = json.load(f)
        else:
            yaml = _get_yaml()
            d = yaml.safe_load(f)

    version = d.get("version", 1)
    if version != CONFIG_VERSION:
        raise ValueError(f"Unsupported config version {version}. Expected {CONFIG_VERSION}.")

    birthdate = _parse_date(d["birthdate"])
    size = _parse_papersize(d.get("size"))
    dpi = d.get("dpi", 300)
    label_space_epsilon = d.get("label_space_epsilon", 0.2)
    max_age = d.get("max_age", 90)

    graph = cls(birthdate, size=size, dpi=dpi,
                label_space_epsilon=label_space_epsilon, max_age=max_age)

    # Title
    title = d.get("title")
    if title is not None:
        if isinstance(title, str):
            graph.add_title(title)
        elif isinstance(title, dict):
            graph.add_title(title["text"], fontsize=title.get("fontsize"))

    # Watermark
    watermark = d.get("watermark")
    if watermark is not None:
        graph.add_watermark(watermark)

    # Image
    image = d.get("image")
    if image is not None:
        graph.add_image(image["path"], alpha=image.get("alpha", 1))

    # Show max age label
    if d.get("show_max_age_label"):
        graph.show_max_age_label()

    # Events
    for ev in d.get("events", []):
        graph.add_life_event(
            text=ev["text"],
            date=_parse_date(ev["date"]),
            color=_parse_color(ev.get("color")),
            hint=_parse_hint(ev.get("hint")),
            side=_parse_side(ev.get("side")),
            color_square=ev.get("color_square", True),
        )

    # Eras
    for era in d.get("eras", []):
        graph.add_era(
            text=era["text"],
            start_date=_parse_date(era["start_date"]),
            end_date=_parse_date(era["end_date"]),
            color=_parse_color(era.get("color")),
            side=_parse_side(era.get("side")),
            alpha=era.get("alpha", 0.3),
        )

    # Era spans
    for span in d.get("era_spans", []):
        graph.add_era_span(
            text=span["text"],
            start_date=_parse_date(span["start_date"]),
            end_date=_parse_date(span["end_date"]),
            color=_parse_color(span.get("color")),
            hint=_parse_hint(span.get("hint")),
            side=_parse_side(span.get("side")),
            color_start_and_end_markers=span.get("color_start_and_end_markers", False),
        )

    # Styling
    if apply_styling and "styling" in d:
        styling = d["styling"]
        if "x_axis" in styling:
            x = styling["x_axis"]
            graph.format_x_axis(
                text=x.get("text"),
                positionx=x.get("positionx"),
                positiony=x.get("positiony"),
                color=_parse_color(x.get("color")),
                fontsize=x.get("fontsize"),
            )
        if "y_axis" in styling:
            y = styling["y_axis"]
            graph.format_y_axis(
                text=y.get("text"),
                positionx=y.get("positionx"),
                positiony=y.get("positiony"),
                color=_parse_color(y.get("color")),
                fontsize=y.get("fontsize"),
            )

    return graph
