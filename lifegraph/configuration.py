from enum import Enum
from pathlib import Path

import matplotlib

_STYLES_DIR = Path(__file__).resolve().parent / "styles"
STYLE_PATH = _STYLES_DIR / "lifegraph.mplstyle"

# A3 is the reference size; all other sizes scale relative to its diagonal.
_A3_DIAG = (11.7**2 + 16.5**2) ** 0.5


def _clamp(val, lo, hi):
    return max(lo, min(hi, val))


def _load_base_style():
    """Read the bundled ``.mplstyle`` file and return it as a dict."""
    rc = matplotlib.rc_params_from_file(str(STYLE_PATH), use_default_template=False)
    return dict(rc)


class Papersize(Enum):
    """Supported paper sizes for the life graph figure.

    Each member maps to standard paper dimensions (in inches) that
    determine the default figure size and all proportional styling
    parameters.  ISO A-series sizes range from A0 (33.1 x 46.8 in) to
    A10 (1.0 x 1.5 in).  US sizes include Letter (8.5 x 11 in), Legal,
    JuniorLegal, HalfLetter, Ledger, and Tabloid.  The default for
    :class:`~lifegraph.Lifegraph` is ``Papersize.A3``.

    Examples
    --------
    >>> from lifegraph import Lifegraph
    >>> from lifegraph.configuration import Papersize
    >>> from datetime import date
    >>> g = Lifegraph(date(1990, 1, 1), size=Papersize.Letter)
    """

    A0 = (33.1, 46.8)
    A1 = (23.4, 33.1)
    A2 = (16.5, 23.4)
    A3 = (11.7, 16.5)
    A4 = (8.3, 11.7)
    A5 = (5.8, 8.3)
    A6 = (4.1, 5.8)
    A7 = (2.9, 4.1)
    A8 = (2.0, 2.9)
    A9 = (1.5, 2.0)
    A10 = (1.0, 1.5)
    HalfLetter = (5.5, 8.5)
    Letter = (8.5, 11.0)
    Legal = (8.5, 14.0)
    JuniorLegal = (5.0, 8.0)
    Ledger = (11.0, 17.0)
    Tabloid = (17.0, 11.0)


class LifegraphParams:
    """Drawing parameters scaled to a particular paper size.

    On construction, two dictionaries are populated:

    * ``rcParams`` -- values forwarded to :func:`matplotlib.pyplot.rcParams.update`.
    * ``otherParams`` -- lifegraph-specific styling knobs (annotation offsets,
      watermark size, era-span line widths, etc.).

    Parameters
    ----------
    papersize : Papersize
        The paper size to configure for.

    Attributes
    ----------
    rcParams : dict
        Matplotlib RC parameter overrides.
    otherParams : dict
        Lifegraph-specific styling parameters.

    Examples
    --------
    >>> from lifegraph.configuration import LifegraphParams, Papersize
    >>> params = LifegraphParams(Papersize.A4)
    >>> params.rcParams["figure.figsize"]
    [8.3, 11.7]
    """

    def __init__(self, papersize):
        self.size = papersize
        w, h = papersize.value
        s = (w**2 + h**2) ** 0.5 / _A3_DIAG

        self.rcParams = _load_base_style()
        self.rcParams.update(
            {
                "figure.figsize": [w, h],
                "axes.labelsize": _clamp(round(16 * s), 1, 40),
                "figure.titlesize": _clamp(round(28 * s), 4, 128),
                "font.size": _clamp(round(18 * s), 1, 60),
                "lines.linewidth": round(max(0.2, 0.5 * s), 2),
                "lines.markersize": round(max(0.5, 4.5 * s), 2),
                "lines.markeredgewidth": round(max(0.01, 0.50 * s), 2),
                "xtick.labelsize": _clamp(round(10 * s), 1, 20),
                "ytick.labelsize": _clamp(round(10 * s), 1, 20),
                "savefig.pad_inches": (
                    0.50 if s > 0.8 else (0.25 if s > 0.4 else 0.05)
                ),
            }
        )

        self.otherParams = {
            "xlabel.position": (0.20, 1.05),
            "xlabel.color": None,
            "xlabel.fontsize": None,
            "ylabel.position": (-0.03, 0.95),
            "ylabel.color": None,
            "ylabel.fontsize": None,
            "maxage.fontsize": _clamp(round(20 * s), 2, 38),
            "figure.title.yposition": 0.95 if s > 0.3 else 0.97,
            "annotation.marker.size": round(max(0.001, 8.0 * s), 2),
            "annotation.edge.width": round(max(0.1, 0.8 * s), 2),
            "annotation.line.width": round(max(0.1, 1.0 * s), 2),
            "annotation.shrinkA": 0,
            "annotation.left.offset": 6 if s < 1.5 else 3,
            "annotation.right.offset": 5 if s < 1.5 else 3,
            "era.span.linestyle": "-",
            "era.span.markersize": 0,
            "era.line.linewidth": round(max(0.2, 1.0 * s), 2),
            "watermark.fontsize": _clamp(round(120 * s), 18, 200),
        }
