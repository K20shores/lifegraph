from enum import Enum

class Papersize(Enum):
    """A class holding papersize in inches"""
    A0 = 1, #[33.1, 46.8] inches
    A1 = 2, #[23.4, 33.1] inches
    A2 = 3, #[16.5, 23.4] inches
    A3 = 4, #[11.7, 16.5] inches
    A4 = 5, #[8.3, 11.7] inches
    A5 = 6, #[5.8, 8.3] inches
    A6 = 7, #[4.1, 5.8] inches
    A7 = 8, #[2.9, 4.1] inches
    A8 = 9, #[2.0, 2.9] inches
    A9 = 10, #[1.5, 2.0] inches
    A10 = 11, #[1.0, 1.5] inches
    HalfLetter = 12, #[5.5, 8.5] inches
    Letter = 13, #[8.5, 11.0] inches
    Legal = 14, #[8.5, 14.0] inches
    JuniorLegal = 15, #[5.0, 8.0] inches
    Ledger = 16, #[11.0, 17.0] inches
    Tabloid = 17 #[17.0, 11.0] inches


class LifegraphParams:
    """A class that defines the defaults for drawing by papersize"""

    def __init__(self, papersize):
        d = None
        if papersize == Papersize.A0:
            d = {
                "rcParams": {
                    "axes.labelsize": 34,
                    "axes.labelcolor": 'blue',
                    "axes.linewidth": 0.0,
                    "axes.spines.bottom": False,
                    "axes.spines.left": False,
                    "axes.spines.right": False,
                    "axes.spines.top": False,
                    "figure.figsize": [33.1, 46.8],
                    "figure.titlesize": 128,
                    "font.size": 60,
                    "lines.linestyle": 'none',
                    "lines.linewidth": 1.0,
                    "lines.marker": 's',
                    "lines.markeredgecolor": 'black',
                    "lines.markeredgewidth": 1.00,
                    "lines.markerfacecolor": 'none',
                    "lines.markersize": 12.0,
                    "markers.fillstyle": 'none',
                    "savefig.pad_inches": 0.05,
                    "text.usetex": False,
                    "xtick.bottom": False,
                    "xtick.color": "black",
                    "xtick.labelsize": 20,
                    "xtick.labeltop": True,
                    "xtick.major.bottom": False,
                    "xtick.major.pad": -3,
                    "xtick.major.top": True,
                    "xtick.minor.bottom": False,
                    "xtick.minor.top": False,
                    "xtick.top": False,
                    "ytick.color": "black",
                    "ytick.labelsize": 20,
                    "ytick.left": False,
                    "ytick.major.left": True,
                    "ytick.major.pad": -4,
                    "ytick.major.right": False,
                    "ytick.minor.left": False,
                    "ytick.minor.right": False,
                    "ytick.right": False,
                },
                "otherParams": {
                    "xlabel.position": (0.20, 1.05),
                    "xlabel.color": None,  # defaults to "axes.labelcolor"
                    "xlabel.fontsize": None,  # defaults to "axes.labelsize"
                    "ylabel.position": (-0.02, 0.95),
                    "ylabel.color": None,  # defaults to "axes.labelcolor"
                    "ylabel.fontsize": None,  # defaults to "axes.labelsize"
                    "maxage.fontsize": 38,
                    "figure.title.yposition": 0.95,
                    "annotation.marker.size": 28.0,
                    "annotation.edge.width": 2.0,
                    "annotation.line.width": 2.0,
                    "annotation.shrinkA": 0,
                    #"annotation.shrinkB": 0, this is calculated, see the help for __draw_annotations
                    "annotation.left.offset": 3,
                    "annotation.right.offset": 3,
                    "era.span.linestyle": "-",
                    "era.span.markersize": 0,
                    "era.line.linewidth": 1,
                    "watermark.fontsize": 200
                }
            }
        elif papersize == Papersize.A1:
            d = {
                "rcParams": {
                    "axes.labelsize": 26,
                    "axes.labelcolor": 'blue',
                    "axes.linewidth": 0.0,
                    "axes.spines.bottom": False,
                    "axes.spines.left": False,
                    "axes.spines.right": False,
                    "axes.spines.top": False,
                    "figure.figsize": [23.4, 33.1],
                    "figure.titlesize": 42,
                    "font.size": 28,
                    "lines.linestyle": 'none',
                    "lines.linewidth": 0.5,
                    "lines.marker": 's',
                    "lines.markeredgecolor": 'black',
                    "lines.markeredgewidth": 0.50,
                    "lines.markerfacecolor": 'none',
                    "lines.markersize": 9.0,
                    "markers.fillstyle": 'none',
                    "savefig.pad_inches": 0.25,
                    "text.usetex": False,
                    "xtick.bottom": False,
                    "xtick.color": "black",
                    "xtick.labelsize": 16,
                    "xtick.labeltop": True,
                    "xtick.major.bottom": False,
                    "xtick.major.pad": -3,
                    "xtick.major.top": True,
                    "xtick.minor.bottom": False,
                    "xtick.minor.top": False,
                    "xtick.top": False,
                    "ytick.color": "black",
                    "ytick.labelsize": 16,
                    "ytick.left": False,
                    "ytick.major.left": True,
                    "ytick.major.pad": -4,
                    "ytick.major.right": False,
                    "ytick.minor.left": False,
                    "ytick.minor.right": False,
                    "ytick.right": False,
                },
                "otherParams": {
                    "xlabel.position": (0.20, 1.05),
                    "xlabel.color": None,  # defaults to "axes.labelcolor"
                    "xlabel.fontsize": None,  # defaults to "axes.labelsize"
                    "ylabel.position": (-0.03, 0.95),
                    "ylabel.color": None,  # defaults to "axes.labelcolor"
                    "ylabel.fontsize": None,  # defaults to "axes.labelsize"
                    "maxage.fontsize": 32,
                    "figure.title.yposition": 0.95,
                    "annotation.marker.size": 18.0,
                    "annotation.edge.width": 0.8,
                    "annotation.line.width": 1.0,
                    "annotation.shrinkA": 0,
                    #"annotation.shrinkB": 0, this is calculated, see the help for __draw_annotations
                    "annotation.left.offset": 6,
                    "annotation.right.offset": 5,
                    "era.span.linestyle": "-",
                    "era.span.markersize": 0,
                    "era.line.linewidth": 1,
                    "watermark.fontsize": 160
                }
            }
        elif papersize == Papersize.A2:
            d = {
                "rcParams": {
                    "axes.labelsize": 16,
                    "axes.labelcolor": 'blue',
                    "axes.linewidth": 0.0,
                    "axes.spines.bottom": False,
                    "axes.spines.left": False,
                    "axes.spines.right": False,
                    "axes.spines.top": False,
                    "figure.figsize": [16.5, 23.4],
                    "figure.titlesize": 42,
                    "font.size": 28,
                    "lines.linestyle": 'none',
                    "lines.linewidth": 0.5,
                    "lines.marker": 's',
                    "lines.markeredgecolor": 'black',
                    "lines.markeredgewidth": 0.50,
                    "lines.markerfacecolor": 'none',
                    "lines.markersize": 6.0,
                    "markers.fillstyle": 'none',
                    "savefig.pad_inches": 0.25,
                    "text.usetex": False,
                    "xtick.bottom": False,
                    "xtick.color": "black",
                    "xtick.labelsize": 10,
                    "xtick.labeltop": True,
                    "xtick.major.bottom": False,
                    "xtick.major.pad": -3,
                    "xtick.major.top": True,
                    "xtick.minor.bottom": False,
                    "xtick.minor.top": False,
                    "xtick.top": False,
                    "ytick.color": "black",
                    "ytick.labelsize": 10,
                    "ytick.left": False,
                    "ytick.major.left": True,
                    "ytick.major.pad": -4,
                    "ytick.major.right": False,
                    "ytick.minor.left": False,
                    "ytick.minor.right": False,
                    "ytick.right": False,
                },
                "otherParams": {
                    "xlabel.position": (0.20, 1.05),
                    "xlabel.color": None,  # defaults to "axes.labelcolor"
                    "xlabel.fontsize": None,  # defaults to "axes.labelsize"
                    "ylabel.position": (-0.03, 0.95),
                    "ylabel.color": None,  # defaults to "axes.labelcolor"
                    "ylabel.fontsize": None,  # defaults to "axes.labelsize"
                    "maxage.fontsize": 24,
                    "figure.title.yposition": 0.98,
                    "annotation.marker.size": 6.0,
                    "annotation.edge.width": 0.8,
                    "annotation.line.width": 1.0,
                    "annotation.shrinkA": 0,
                    #"annotation.shrinkB": 0, this is calculated, see the help for __draw_annotations
                    "annotation.left.offset": 6,
                    "annotation.right.offset": 5,
                    "era.span.linestyle": "-",
                    "era.span.markersize": 0,
                    "era.line.linewidth": 1,
                    "watermark.fontsize": 135
                }
            }
        elif papersize == Papersize.A3:
            d = {
                "rcParams": {
                    "axes.labelsize": 16,
                    "axes.labelcolor": 'blue',
                    "axes.linewidth": 0.0,
                    "axes.spines.bottom": False,
                    "axes.spines.left": False,
                    "axes.spines.right": False,
                    "axes.spines.top": False,
                    "figure.figsize": [11.7, 16.5],
                    "figure.titlesize": 28,
                    "font.size": 18,
                    "lines.linestyle": 'none',
                    "lines.linewidth": 0.5,
                    "lines.marker": 's',
                    "lines.markeredgecolor": 'black',
                    "lines.markeredgewidth": 0.50,
                    "lines.markerfacecolor": 'none',
                    "lines.markersize": 4.5,
                    "markers.fillstyle": 'none',
                    "savefig.pad_inches": 0.25,
                    "text.usetex": False,
                    "xtick.bottom": False,
                    "xtick.color": "black",
                    "xtick.labelsize": 10,
                    "xtick.labeltop": True,
                    "xtick.major.bottom": False,
                    "xtick.major.pad": -3,
                    "xtick.major.top": True,
                    "xtick.minor.bottom": False,
                    "xtick.minor.top": False,
                    "xtick.top": False,
                    "ytick.color": "black",
                    "ytick.labelsize": 10,
                    "ytick.left": False,
                    "ytick.major.left": True,
                    "ytick.major.pad": -4,
                    "ytick.major.right": False,
                    "ytick.minor.left": False,
                    "ytick.minor.right": False,
                    "ytick.right": False,
                },
                "otherParams": {
                    "xlabel.position": (0.20, 1.05),
                    "xlabel.color": None,  # defaults to "axes.labelcolor"
                    "xlabel.fontsize": None,  # defaults to "axes.labelsize"
                    "ylabel.position": (-0.03, 0.95),
                    "ylabel.color": None,  # defaults to "axes.labelcolor"
                    "ylabel.fontsize": None,  # defaults to "axes.labelsize"
                    "maxage.fontsize": 20,
                    "figure.title.yposition": 0.95,
                    "annotation.marker.size": 8.0,
                    "annotation.edge.width": 0.8,
                    "annotation.line.width": 1.0,
                    "annotation.shrinkA": 0,
                    #"annotation.shrinkB": 0, this is calculated, see the help for __draw_annotations
                    "annotation.left.offset": 6,
                    "annotation.right.offset": 5,
                    "era.span.linestyle": "-",
                    "era.span.markersize": 0,
                    "era.line.linewidth": 1,
                    "watermark.fontsize": 120
                }
            }
        elif papersize == Papersize.A4:
            d = {
                "rcParams": {
                    "axes.labelsize": 12,
                    "axes.labelcolor": 'blue',
                    "axes.linewidth": 0.0,
                    "axes.spines.bottom": False,
                    "axes.spines.left": False,
                    "axes.spines.right": False,
                    "axes.spines.top": False,
                    "figure.figsize": [8.3, 11.7],
                    "figure.titlesize": 24,
                    "font.size": 16,
                    "lines.linestyle": 'none',
                    "lines.linewidth": 0.5,
                    "lines.marker": 's',
                    "lines.markeredgecolor": 'black',
                    "lines.markeredgewidth": 0.50,
                    "lines.markerfacecolor": 'none',
                    "lines.markersize": 3.0,
                    "markers.fillstyle": 'none',
                    "savefig.pad_inches": 0.05,
                    "text.usetex": False,
                    "xtick.bottom": False,
                    "xtick.color": "black",
                    "xtick.labelsize": 10,
                    "xtick.labeltop": True,
                    "xtick.major.bottom": False,
                    "xtick.major.pad": -3,
                    "xtick.major.top": True,
                    "xtick.minor.bottom": False,
                    "xtick.minor.top": False,
                    "xtick.top": False,
                    "ytick.color": "black",
                    "ytick.labelsize": 10,
                    "ytick.left": False,
                    "ytick.major.left": True,
                    "ytick.major.pad": -4,
                    "ytick.major.right": False,
                    "ytick.minor.left": False,
                    "ytick.minor.right": False,
                    "ytick.right": False,
                },
                "otherParams": {
                    "xlabel.position": (0.20, 1.05),
                    "xlabel.color": None,  # defaults to "axes.labelcolor"
                    "xlabel.fontsize": None,  # defaults to "axes.labelsize"
                    "ylabel.position": (-0.03, 0.95),
                    "ylabel.color": None,  # defaults to "axes.labelcolor"
                    "ylabel.fontsize": None,  # defaults to "axes.labelsize"
                    "maxage.fontsize": 16,
                    "figure.title.yposition": 0.95,
                    "annotation.marker.size": 6.0,
                    "annotation.edge.width": 0.8,
                    "annotation.line.width": 1.0,
                    "annotation.shrinkA": 0,
                    #"annotation.shrinkB": 0, this is calculated, see the help for __draw_annotations
                    "annotation.left.offset": 6,
                    "annotation.right.offset": 5,
                    "era.span.linestyle": "-",
                    "era.span.markersize": 0,
                    "era.line.linewidth": 1,
                    "watermark.fontsize": 110
                }
            }
        elif papersize == Papersize.A5:
            d = {
                "rcParams": {
                    "axes.labelsize": 8,
                    "axes.labelcolor": 'blue',
                    "axes.linewidth": 0.0,
                    "axes.spines.bottom": False,
                    "axes.spines.left": False,
                    "axes.spines.right": False,
                    "axes.spines.top": False,
                    "figure.figsize": [5.8, 8.3],
                    "figure.titlesize": 20,
                    "font.size": 10,
                    "lines.linestyle": 'none',
                    "lines.linewidth": 0.5,
                    "lines.marker": 's',
                    "lines.markeredgecolor": 'black',
                    "lines.markeredgewidth": 0.20,
                    "lines.markerfacecolor": 'none',
                    "lines.markersize": 2.0,
                    "markers.fillstyle": 'none',
                    "savefig.pad_inches": 0.05,
                    "text.usetex": False,
                    "xtick.bottom": False,
                    "xtick.color": "black",
                    "xtick.labelsize": 6,
                    "xtick.labeltop": True,
                    "xtick.major.bottom": False,
                    "xtick.major.pad": -3,
                    "xtick.major.top": True,
                    "xtick.minor.bottom": False,
                    "xtick.minor.top": False,
                    "xtick.top": False,
                    "ytick.color": "black",
                    "ytick.labelsize": 6,
                    "ytick.left": False,
                    "ytick.major.left": True,
                    "ytick.major.pad": -4,
                    "ytick.major.right": False,
                    "ytick.minor.left": False,
                    "ytick.minor.right": False,
                    "ytick.right": False,
                },
                "otherParams": {
                    "xlabel.position": (0.20, 1.05),
                    "xlabel.color": None,  # defaults to "axes.labelcolor"
                    "xlabel.fontsize": None,  # defaults to "axes.labelsize"
                    "ylabel.position": (-0.03, 0.95),
                    "ylabel.color": None,  # defaults to "axes.labelcolor"
                    "ylabel.fontsize": None,  # defaults to "axes.labelsize"
                    "maxage.fontsize": 10,
                    "figure.title.yposition": 0.97,
                    "annotation.marker.size": 6.0,
                    "annotation.edge.width": 0.8,
                    "annotation.line.width": 1.0,
                    "annotation.shrinkA": 0,
                    #"annotation.shrinkB": 0, this is calculated, see the help for __draw_annotations
                    "annotation.left.offset": 6,
                    "annotation.right.offset": 5,
                    "era.span.linestyle": "-",
                    "era.span.markersize": 0,
                    "era.line.linewidth": 1,
                    "watermark.fontsize": 90
                }
            }
        elif papersize == Papersize.A6:
            d = {
                "rcParams": {
                    "axes.labelsize": 7,
                    "axes.labelcolor": 'blue',
                    "axes.linewidth": 0.0,
                    "axes.spines.bottom": False,
                    "axes.spines.left": False,
                    "axes.spines.right": False,
                    "axes.spines.top": False,
                    "figure.figsize": [4.1, 5.8],
                    "figure.titlesize": 18,
                    "font.size": 9,
                    "lines.linestyle": 'none',
                    "lines.linewidth": 0.3,
                    "lines.marker": 's',
                    "lines.markeredgecolor": 'black',
                    "lines.markeredgewidth": 0.25,
                    "lines.markerfacecolor": 'none',
                    "lines.markersize": 1.25,
                    "markers.fillstyle": 'none',
                    "savefig.pad_inches": 0.05,
                    "text.usetex": False,
                    "xtick.bottom": False,
                    "xtick.color": "black",
                    "xtick.labelsize": 4,
                    "xtick.labeltop": True,
                    "xtick.major.bottom": False,
                    "xtick.major.pad": -3,
                    "xtick.major.top": True,
                    "xtick.minor.bottom": False,
                    "xtick.minor.top": False,
                    "xtick.top": False,
                    "ytick.color": "black",
                    "ytick.labelsize": 4,
                    "ytick.left": False,
                    "ytick.major.left": True,
                    "ytick.major.pad": -4,
                    "ytick.major.right": False,
                    "ytick.minor.left": False,
                    "ytick.minor.right": False,
                    "ytick.right": False,
                },
                "otherParams": {
                    "xlabel.position": (0.20, 1.05),
                    "xlabel.color": None,  # defaults to "axes.labelcolor"
                    "xlabel.fontsize": None,  # defaults to "axes.labelsize"
                    "ylabel.position": (-0.03, 0.95),
                    "ylabel.color": None,  # defaults to "axes.labelcolor"
                    "ylabel.fontsize": None,  # defaults to "axes.labelsize"
                    "maxage.fontsize": 8,
                    "figure.title.yposition": 0.97,
                    "annotation.marker.size": 2.0,
                    "annotation.edge.width": 0.6,
                    "annotation.line.width": 0.5,
                    "annotation.shrinkA": 0,
                    #"annotation.shrinkB": 0, this is calculated, see the help for __draw_annotations
                    "annotation.left.offset": 6,
                    "annotation.right.offset": 5,
                    "era.span.linestyle": "-",
                    "era.span.markersize": 0,
                    "era.line.linewidth": 0.5,
                    "watermark.fontsize": 70
                }
            }
        elif papersize == Papersize.A7:
            d = {
                "rcParams": {
                    "axes.labelsize": 3,
                    "axes.labelcolor": 'blue',
                    "axes.linewidth": 0.0,
                    "axes.spines.bottom": False,
                    "axes.spines.left": False,
                    "axes.spines.right": False,
                    "axes.spines.top": False,
                    "figure.figsize": [2.9, 4.1],
                    "figure.titlesize": 12,
                    "font.size": 5,
                    "lines.linestyle": 'none',
                    "lines.linewidth": 0.2,
                    "lines.marker": 's',
                    "lines.markeredgecolor": 'black',
                    "lines.markeredgewidth": 0.20,
                    "lines.markerfacecolor": 'none',
                    "lines.markersize": 1.0,
                    "markers.fillstyle": 'none',
                    "savefig.pad_inches": 0.05,
                    "text.usetex": False,
                    "xtick.bottom": False,
                    "xtick.color": "black",
                    "xtick.labelsize": 3,
                    "xtick.labeltop": True,
                    "xtick.major.bottom": False,
                    "xtick.major.pad": -3,
                    "xtick.major.top": True,
                    "xtick.minor.bottom": False,
                    "xtick.minor.top": False,
                    "xtick.top": False,
                    "ytick.color": "black",
                    "ytick.labelsize": 3,
                    "ytick.left": False,
                    "ytick.major.left": True,
                    "ytick.major.pad": -4,
                    "ytick.major.right": False,
                    "ytick.minor.left": False,
                    "ytick.minor.right": False,
                    "ytick.right": False,
                },
                "otherParams": {
                    "xlabel.position": (0.20, 1.05),
                    "xlabel.color": None,  # defaults to "axes.labelcolor"
                    "xlabel.fontsize": None,  # defaults to "axes.labelsize"
                    "ylabel.position": (-0.03, 0.95),
                    "ylabel.color": None,  # defaults to "axes.labelcolor"
                    "ylabel.fontsize": None,  # defaults to "axes.labelsize"
                    "maxage.fontsize": 6,
                    "figure.title.yposition": 0.95,
                    "annotation.marker.size": 2.0,
                    "annotation.edge.width": 0.3,
                    "annotation.line.width": 0.5,
                    "annotation.shrinkA": 0,
                    #"annotation.shrinkB": 0, this is calculated, see the help for __draw_annotations
                    "annotation.left.offset": 6,
                    "annotation.right.offset": 5,
                    "era.span.linestyle": "-",
                    "era.span.markersize": 0,
                    "era.line.linewidth": 0.5,
                    "watermark.fontsize": 50
                }
            }
        elif papersize == Papersize.A8:
            d = {
                "rcParams": {
                    "axes.labelsize": 2,
                    "axes.labelcolor": 'blue',
                    "axes.linewidth": 0.0,
                    "axes.spines.bottom": False,
                    "axes.spines.left": False,
                    "axes.spines.right": False,
                    "axes.spines.top": False,
                    "figure.figsize": [2.0, 2.9],
                    "figure.titlesize": 6,
                    "font.size": 3,
                    "lines.linestyle": 'none',
                    "lines.linewidth": 0.2,
                    "lines.marker": 's',
                    "lines.markeredgecolor": 'black',
                    "lines.markeredgewidth": 0.15,
                    "lines.markerfacecolor": 'none',
                    "lines.markersize": 0.6,
                    "markers.fillstyle": 'none',
                    "savefig.pad_inches": 0.05,
                    "text.usetex": False,
                    "xtick.bottom": False,
                    "xtick.color": "black",
                    "xtick.labelsize": 2,
                    "xtick.labeltop": True,
                    "xtick.major.bottom": False,
                    "xtick.major.pad": -3,
                    "xtick.major.top": True,
                    "xtick.minor.bottom": False,
                    "xtick.minor.top": False,
                    "xtick.top": False,
                    "ytick.color": "black",
                    "ytick.labelsize": 2,
                    "ytick.left": False,
                    "ytick.major.left": True,
                    "ytick.major.pad": -4,
                    "ytick.major.right": False,
                    "ytick.minor.left": False,
                    "ytick.minor.right": False,
                    "ytick.right": False,
                },
                "otherParams": {
                    "xlabel.position": (0.20, 1.05),
                    "xlabel.color": None,  # defaults to "axes.labelcolor"
                    "xlabel.fontsize": None,  # defaults to "axes.labelsize"
                    "ylabel.position": (-0.03, 0.95),
                    "ylabel.color": None,  # defaults to "axes.labelcolor"
                    "ylabel.fontsize": None,  # defaults to "axes.labelsize"
                    "maxage.fontsize": 3,
                    "figure.title.yposition": 0.95,
                    "annotation.marker.size": 1.8,
                    "annotation.edge.width": 0.3,
                    "annotation.line.width": 0.3,
                    "annotation.shrinkA": 0,
                    #"annotation.shrinkB": 0, this is calculated, see the help for __draw_annotations
                    "annotation.left.offset": 6,
                    "annotation.right.offset": 5,
                    "era.span.linestyle": "-",
                    "era.span.markersize": 0,
                    "era.line.linewidth": 0.5,
                    "watermark.fontsize": 35
                }
            }
        elif papersize == Papersize.A9:
            d = {
                "rcParams": {
                    "axes.labelsize": 2,
                    "axes.labelcolor": 'blue',
                    "axes.linewidth": 0.0,
                    "axes.spines.bottom": False,
                    "axes.spines.left": False,
                    "axes.spines.right": False,
                    "axes.spines.top": False,
                    "figure.figsize": [1.5, 2.0],
                    "figure.titlesize": 5,
                    "font.size": 3,
                    "lines.linestyle": 'none',
                    "lines.linewidth": 0.2,
                    "lines.marker": 's',
                    "lines.markeredgecolor": 'black',
                    "lines.markeredgewidth": 0.10,
                    "lines.markerfacecolor": 'none',
                    "lines.markersize": 0.54,
                    "markers.fillstyle": 'none',
                    "savefig.pad_inches": 0.05,
                    "text.usetex": False,
                    "xtick.bottom": False,
                    "xtick.color": "black",
                    "xtick.labelsize": 1,
                    "xtick.labeltop": True,
                    "xtick.major.bottom": False,
                    "xtick.major.pad": -3,
                    "xtick.major.top": True,
                    "xtick.minor.bottom": False,
                    "xtick.minor.top": False,
                    "xtick.top": False,
                    "ytick.color": "black",
                    "ytick.labelsize": 1,
                    "ytick.left": False,
                    "ytick.major.left": True,
                    "ytick.major.pad": -4,
                    "ytick.major.right": False,
                    "ytick.minor.left": False,
                    "ytick.minor.right": False,
                    "ytick.right": False,
                },
                "otherParams": {
                    "xlabel.position": (0.20, 1.05),
                    "xlabel.color": None,  # defaults to "axes.labelcolor"
                    "xlabel.fontsize": None,  # defaults to "axes.labelsize"
                    "ylabel.position": (-0.03, 0.95),
                    "ylabel.color": None,  # defaults to "axes.labelcolor"
                    "ylabel.fontsize": None,  # defaults to "axes.labelsize"
                    "maxage.fontsize": 2,
                    "figure.title.yposition": 0.95,
                    "annotation.marker.size": 1.2,
                    "annotation.edge.width": 0.2,
                    "annotation.line.width": 0.2,
                    "annotation.shrinkA": 0,
                    #"annotation.shrinkB": 0, this is calculated, see the help for __draw_annotations
                    "annotation.left.offset": 6,
                    "annotation.right.offset": 5,
                    "era.span.linestyle": "-",
                    "era.span.markersize": 0,
                    "era.line.linewidth": 0.5,
                    "watermark.fontsize": 30
                }
            }
        elif papersize == Papersize.A10:
            d = {
                "rcParams": {
                    "axes.labelsize": 2,
                    "axes.labelcolor": 'blue',
                    "axes.linewidth": 0.0,
                    "axes.spines.bottom": False,
                    "axes.spines.left": False,
                    "axes.spines.right": False,
                    "axes.spines.top": False,
                    "figure.figsize": [1.0, 1.5],
                    "figure.titlesize": 4,
                    "font.size": 1,
                    "lines.linestyle": 'none',
                    "lines.linewidth": 0.5,
                    "lines.marker": 's',
                    "lines.markeredgecolor": 'black',
                    "lines.markeredgewidth": 0.01,
                    "lines.markerfacecolor": 'none',
                    "lines.markersize": 0.50,
                    "markers.fillstyle": 'none',
                    "savefig.pad_inches": 0.05,
                    "text.usetex": False,
                    "xtick.bottom": False,
                    "xtick.color": "black",
                    "xtick.labelsize": 1,
                    "xtick.labeltop": True,
                    "xtick.major.bottom": False,
                    "xtick.major.pad": -3,
                    "xtick.major.top": True,
                    "xtick.minor.bottom": False,
                    "xtick.minor.top": False,
                    "xtick.top": False,
                    "ytick.color": "black",
                    "ytick.labelsize": 1,
                    "ytick.left": False,
                    "ytick.major.left": True,
                    "ytick.major.pad": -4,
                    "ytick.major.right": False,
                    "ytick.minor.left": False,
                    "ytick.minor.right": False,
                    "ytick.right": False,
                },
                "otherParams": {
                    "xlabel.position": (0.20, 1.05),
                    "xlabel.color": None,  # defaults to "axes.labelcolor"
                    "xlabel.fontsize": None,  # defaults to "axes.labelsize"
                    "ylabel.position": (-0.02, 0.95),
                    "ylabel.color": None,  # defaults to "axes.labelcolor"
                    "ylabel.fontsize": None,  # defaults to "axes.labelsize"
                    "maxage.fontsize": 2,
                    "figure.title.yposition": 0.95,
                    "annotation.marker.size": .001,
                    "annotation.edge.width": 0.1,
                    "annotation.line.width": 0.1,
                    "annotation.shrinkA": 0,
                    #"annotation.shrinkB": 0, this is calculated, see the help for __draw_annotations
                    "annotation.left.offset": 5,
                    "annotation.right.offset": 5,
                    "era.span.linestyle": "-",
                    "era.span.markersize": 0,
                    "era.line.linewidth": .2,
                    "watermark.fontsize": 18
                }
            }
        elif papersize == Papersize.HalfLetter:
            d = {
                "rcParams": {
                    "axes.labelsize": 8,
                    "axes.labelcolor": 'blue',
                    "axes.linewidth": 0.0,
                    "axes.spines.bottom": False,
                    "axes.spines.left": False,
                    "axes.spines.right": False,
                    "axes.spines.top": False,
                    "figure.figsize": [5.5, 8.5],
                    "figure.titlesize": 20,
                    "font.size": 10,
                    "lines.linestyle": 'none',
                    "lines.linewidth": 0.5,
                    "lines.marker": 's',
                    "lines.markeredgecolor": 'black',
                    "lines.markeredgewidth": 0.30,
                    "lines.markerfacecolor": 'none',
                    "lines.markersize": 1.5,
                    "markers.fillstyle": 'none',
                    "savefig.pad_inches": 0.05,
                    "text.usetex": False,
                    "xtick.bottom": False,
                    "xtick.color": "black",
                    "xtick.labelsize": 5,
                    "xtick.labeltop": True,
                    "xtick.major.bottom": False,
                    "xtick.major.pad": -3,
                    "xtick.major.top": True,
                    "xtick.minor.bottom": False,
                    "xtick.minor.top": False,
                    "xtick.top": False,
                    "ytick.color": "black",
                    "ytick.labelsize": 5,
                    "ytick.left": False,
                    "ytick.major.left": True,
                    "ytick.major.pad": -4,
                    "ytick.major.right": False,
                    "ytick.minor.left": False,
                    "ytick.minor.right": False,
                    "ytick.right": False,
                },
                "otherParams": {
                    "xlabel.position": (0.20, 1.05),
                    "xlabel.color": None,  # defaults to "axes.labelcolor"
                    "xlabel.fontsize": None,  # defaults to "axes.labelsize"
                    "ylabel.position": (-0.03, 0.95),
                    "ylabel.color": None,  # defaults to "axes.labelcolor"
                    "ylabel.fontsize": None,  # defaults to "axes.labelsize"
                    "maxage.fontsize": 10,
                    "figure.title.yposition": 0.95,
                    "annotation.marker.size": 6.0,
                    "annotation.edge.width": 0.8,
                    "annotation.line.width": 1.0,
                    "annotation.shrinkA": 0,
                    #"annotation.shrinkB": 0, this is calculated, see the help for __draw_annotations
                    "annotation.left.offset": 6,
                    "annotation.right.offset": 5,
                    "era.span.linestyle": "-",
                    "era.span.markersize": 0,
                    "era.line.linewidth": 1,
                    "watermark.fontsize": 90
                }
            }
        elif papersize == Papersize.Letter:
            d = {
                "rcParams": {
                    "axes.labelsize": 8,
                    "axes.labelcolor": 'blue',
                    "axes.linewidth": 0.0,
                    "axes.spines.bottom": False,
                    "axes.spines.left": False,
                    "axes.spines.right": False,
                    "axes.spines.top": False,
                    "figure.figsize": [8.5, 11.0],
                    "figure.titlesize": 20,
                    "font.size": 12,
                    "lines.linestyle": 'none',
                    "lines.linewidth": 0.5,
                    "lines.marker": 's',
                    "lines.markeredgecolor": 'black',
                    "lines.markeredgewidth": 0.30,
                    "lines.markerfacecolor": 'none',
                    "lines.markersize": 3.0,
                    "markers.fillstyle": 'none',
                    "savefig.pad_inches": 0.50,
                    "text.usetex": False,
                    "xtick.bottom": False,
                    "xtick.color": "black",
                    "xtick.labelsize": 5,
                    "xtick.labeltop": True,
                    "xtick.major.bottom": False,
                    "xtick.major.pad": -3,
                    "xtick.major.top": True,
                    "xtick.minor.bottom": False,
                    "xtick.minor.top": False,
                    "xtick.top": False,
                    "ytick.color": "black",
                    "ytick.labelsize": 5,
                    "ytick.left": False,
                    "ytick.major.left": True,
                    "ytick.major.pad": -4,
                    "ytick.major.right": False,
                    "ytick.minor.left": False,
                    "ytick.minor.right": False,
                    "ytick.right": False,
                },
                "otherParams": {
                    "xlabel.position": (0.20, 1.05),
                    "xlabel.color": None,  # defaults to "axes.labelcolor"
                    "xlabel.fontsize": None,  # defaults to "axes.labelsize"
                    "ylabel.position": (-0.03, 0.95),
                    "ylabel.color": None,  # defaults to "axes.labelcolor"
                    "ylabel.fontsize": None,  # defaults to "axes.labelsize"
                    "maxage.fontsize": 12,
                    "figure.title.yposition": 0.95,
                    "annotation.marker.size": 6.0,
                    "annotation.edge.width": 0.8,
                    "annotation.line.width": 1.0,
                    "annotation.shrinkA": 0,
                    #"annotation.shrinkB": 0, this is calculated, see the help for __draw_annotations
                    "annotation.left.offset": 3,
                    "annotation.right.offset": 3,
                    "era.span.linestyle": "-",
                    "era.span.markersize": 0,
                    "era.line.linewidth": 1,
                    "watermark.fontsize": 110
                }
            }
        elif papersize == Papersize.Legal:
            d = {
                "rcParams": {
                    "axes.labelsize": 8,
                    "axes.labelcolor": 'blue',
                    "axes.linewidth": 0.0,
                    "axes.spines.bottom": False,
                    "axes.spines.left": False,
                    "axes.spines.right": False,
                    "axes.spines.top": False,
                    "figure.figsize": [8.5, 14.0],
                    "figure.titlesize": 24,
                    "font.size": 12,
                    "lines.linestyle": 'none',
                    "lines.linewidth": 0.5,
                    "lines.marker": 's',
                    "lines.markeredgecolor": 'black',
                    "lines.markeredgewidth": 0.35,
                    "lines.markerfacecolor": 'none',
                    "lines.markersize": 3.0,
                    "markers.fillstyle": 'none',
                    "savefig.pad_inches": 0.50,
                    "text.usetex": False,
                    "xtick.bottom": False,
                    "xtick.color": "black",
                    "xtick.labelsize": 5,
                    "xtick.labeltop": True,
                    "xtick.major.bottom": False,
                    "xtick.major.pad": -3,
                    "xtick.major.top": True,
                    "xtick.minor.bottom": False,
                    "xtick.minor.top": False,
                    "xtick.top": False,
                    "ytick.color": "black",
                    "ytick.labelsize": 5,
                    "ytick.left": False,
                    "ytick.major.left": True,
                    "ytick.major.pad": -4,
                    "ytick.major.right": False,
                    "ytick.minor.left": False,
                    "ytick.minor.right": False,
                    "ytick.right": False,
                },
                "otherParams": {
                    "xlabel.position": (0.20, 1.05),
                    "xlabel.color": None,  # defaults to "axes.labelcolor"
                    "xlabel.fontsize": None,  # defaults to "axes.labelsize"
                    "ylabel.position": (-0.03, 0.95),
                    "ylabel.color": None,  # defaults to "axes.labelcolor"
                    "ylabel.fontsize": None,  # defaults to "axes.labelsize"
                    "maxage.fontsize": 14,
                    "figure.title.yposition": 0.95,
                    "annotation.marker.size": 6.0,
                    "annotation.edge.width": 0.8,
                    "annotation.line.width": 1.0,
                    "annotation.shrinkA": 0,
                    #"annotation.shrinkB": 0, this is calculated, see the help for __draw_annotations
                    "annotation.left.offset": 3,
                    "annotation.right.offset": 2,
                    "era.span.linestyle": "-",
                    "era.span.markersize": 0,
                    "era.line.linewidth": 1,
                    "watermark.fontsize": 110
                }
            }
        elif papersize == Papersize.JuniorLegal:
            d = {
                "rcParams": {
                    "axes.labelsize": 8,
                    "axes.labelcolor": 'blue',
                    "axes.linewidth": 0.0,
                    "axes.spines.bottom": False,
                    "axes.spines.left": False,
                    "axes.spines.right": False,
                    "axes.spines.top": False,
                    "figure.figsize": [5.0, 8.0],
                    "figure.titlesize": 20,
                    "font.size": 10,
                    "lines.linestyle": 'none',
                    "lines.linewidth": 0.5,
                    "lines.marker": 's',
                    "lines.markeredgecolor": 'black',
                    "lines.markeredgewidth": 0.35,
                    "lines.markerfacecolor": 'none',
                    "lines.markersize": 1.5,
                    "markers.fillstyle": 'none',
                    "savefig.pad_inches": 0.50,
                    "text.usetex": False,
                    "xtick.bottom": False,
                    "xtick.color": "black",
                    "xtick.labelsize": 5,
                    "xtick.labeltop": True,
                    "xtick.major.bottom": False,
                    "xtick.major.pad": -3,
                    "xtick.major.top": True,
                    "xtick.minor.bottom": False,
                    "xtick.minor.top": False,
                    "xtick.top": False,
                    "ytick.color": "black",
                    "ytick.labelsize": 5,
                    "ytick.left": False,
                    "ytick.major.left": True,
                    "ytick.major.pad": -4,
                    "ytick.major.right": False,
                    "ytick.minor.left": False,
                    "ytick.minor.right": False,
                    "ytick.right": False,
                },
                "otherParams": {
                    "xlabel.position": (0.20, 1.05),
                    "xlabel.color": None,  # defaults to "axes.labelcolor"
                    "xlabel.fontsize": None,  # defaults to "axes.labelsize"
                    "ylabel.position": (-0.03, 0.95),
                    "ylabel.color": None,  # defaults to "axes.labelcolor"
                    "ylabel.fontsize": None,  # defaults to "axes.labelsize"
                    "maxage.fontsize": 10,
                    "figure.title.yposition": 0.95,
                    "annotation.marker.size": 6.0,
                    "annotation.edge.width": 0.8,
                    "annotation.line.width": 1.0,
                    "annotation.shrinkA": 0,
                    #"annotation.shrinkB": 0, this is calculated, see the help for __draw_annotations
                    "annotation.left.offset": 3,
                    "annotation.right.offset": 2,
                    "era.span.linestyle": "-",
                    "era.span.markersize": 0,
                    "era.line.linewidth": 1,
                    "watermark.fontsize": 75
                }
            }
        elif papersize == Papersize.Ledger:
            d = {
                "rcParams": {
                    "axes.labelsize": 12,
                    "axes.labelcolor": 'blue',
                    "axes.linewidth": 0.0,
                    "axes.spines.bottom": False,
                    "axes.spines.left": False,
                    "axes.spines.right": False,
                    "axes.spines.top": False,
                    "figure.figsize": [11.0, 17.0],
                    "figure.titlesize": 24,
                    "font.size": 18,
                    "lines.linestyle": 'none',
                    "lines.linewidth": 0.5,
                    "lines.marker": 's',
                    "lines.markeredgecolor": 'black',
                    "lines.markeredgewidth": 0.40,
                    "lines.markerfacecolor": 'none',
                    "lines.markersize": 4.0,
                    "markers.fillstyle": 'none',
                    "savefig.pad_inches": 0.50,
                    "text.usetex": False,
                    "xtick.bottom": False,
                    "xtick.color": "black",
                    "xtick.labelsize": 8,
                    "xtick.labeltop": True,
                    "xtick.major.bottom": False,
                    "xtick.major.pad": -3,
                    "xtick.major.top": True,
                    "xtick.minor.bottom": False,
                    "xtick.minor.top": False,
                    "xtick.top": False,
                    "ytick.color": "black",
                    "ytick.labelsize": 8,
                    "ytick.left": False,
                    "ytick.major.left": True,
                    "ytick.major.pad": -4,
                    "ytick.major.right": False,
                    "ytick.minor.left": False,
                    "ytick.minor.right": False,
                    "ytick.right": False,
                },
                "otherParams": {
                    "xlabel.position": (0.20, 1.05),
                    "xlabel.color": None,  # defaults to "axes.labelcolor"
                    "xlabel.fontsize": None,  # defaults to "axes.labelsize"
                    "ylabel.position": (-0.03, 0.95),
                    "ylabel.color": None,  # defaults to "axes.labelcolor"
                    "ylabel.fontsize": None,  # defaults to "axes.labelsize"
                    "maxage.fontsize": 16,
                    "figure.title.yposition": 0.95,
                    "annotation.marker.size": 10.0,
                    "annotation.edge.width": 0.8,
                    "annotation.line.width": 1.0,
                    "annotation.shrinkA": 0,
                    #"annotation.shrinkB": 0, this is calculated, see the help for __draw_annotations
                    "annotation.left.offset": 3,
                    "annotation.right.offset": 2,
                    "era.span.linestyle": "-",
                    "era.span.markersize": 0,
                    "era.line.linewidth": 1,
                    "watermark.fontsize": 110
                }
            }
        elif papersize == Papersize.Tabloid:
            d = {
                "rcParams": {
                    "axes.labelsize": 10,
                    "axes.labelcolor": 'blue',
                    "axes.linewidth": 0.0,
                    "axes.spines.bottom": False,
                    "axes.spines.left": False,
                    "axes.spines.right": False,
                    "axes.spines.top": False,
                    "figure.figsize": [17.0, 11.0],
                    "figure.titlesize": 22,
                    "font.size": 10,
                    "lines.linestyle": 'none',
                    "lines.linewidth": 0.5,
                    "lines.marker": 's',
                    "lines.markeredgecolor": 'black',
                    "lines.markeredgewidth": 0.40,
                    "lines.markerfacecolor": 'none',
                    "lines.markersize": 4.0,
                    "markers.fillstyle": 'none',
                    "savefig.pad_inches": 0.50,
                    "text.usetex": False,
                    "xtick.bottom": False,
                    "xtick.color": "black",
                    "xtick.labelsize": 8,
                    "xtick.labeltop": True,
                    "xtick.major.bottom": False,
                    "xtick.major.pad": -3,
                    "xtick.major.top": True,
                    "xtick.minor.bottom": False,
                    "xtick.minor.top": False,
                    "xtick.top": False,
                    "ytick.color": "black",
                    "ytick.labelsize": 8,
                    "ytick.left": False,
                    "ytick.major.left": True,
                    "ytick.major.pad": -4,
                    "ytick.major.right": False,
                    "ytick.minor.left": False,
                    "ytick.minor.right": False,
                    "ytick.right": False,
                },
                "otherParams": {
                    "xlabel.position": (0.20, 1.05),
                    "xlabel.color": None,  # defaults to "axes.labelcolor"
                    "xlabel.fontsize": None,  # defaults to "axes.labelsize"
                    "ylabel.position": (-0.03, 0.95),
                    "ylabel.color": None,  # defaults to "axes.labelcolor"
                    "ylabel.fontsize": None,  # defaults to "axes.labelsize"
                    "maxage.fontsize": 16,
                    "figure.title.yposition": 0.97,
                    "annotation.marker.size": 10.0,
                    "annotation.edge.width": 0.8,
                    "annotation.line.width": 1.0,
                    "annotation.shrinkA": 0,
                    #"annotation.shrinkB": 0, this is calculated, see the help for __draw_annotations
                    "annotation.left.offset": 6,
                    "annotation.right.offset": 6,
                    "era.span.linestyle": "-",
                    "era.span.markersize": 0,
                    "era.line.linewidth": 1,
                    "watermark.fontsize": 130
                }
            }
        else:
            raise ValueError("Unknown paper size")

        self.settings = d
        self.size = papersize
        self.rcParams = d["rcParams"]
        self.otherParams = d["otherParams"]
