from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date
from pathlib import Path

IMAGES_DIR = Path(__file__).parent / "images"

def main(path=None):
    birthday = date(1990, 11, 1)
    g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

    g.add_title("Time is Not Equal to Money")
    g.show_max_age_label()

    # Users can customize via the settings dict
    g.settings.rcParams["lines.marker"] = 'v'
    g.settings.rcParams["lines.markersize"] = 2.0

    # Or use matplotlib's style system with the bundled style:
    # from lifegraph.configuration import STYLE_PATH
    # plt.style.use(STYLE_PATH)

    output = Path(path) / "grid_customization.png" if path else IMAGES_DIR / "grid_customization.png"
    g.save(str(output))

if __name__ == '__main__':
    main()

def test_grid_customization(tmp_path):
    main(tmp_path)
