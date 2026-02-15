from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date
from pathlib import Path

IMAGES_DIR = Path(__file__).parent / "images"

def main(path=None):
    birthday = date(1990, 11, 1)
    g = Lifegraph(birthday, dpi=300, size=Papersize.A4, axes_rect=[.1, .1, .8, .8])
    output = Path(path) / "grid.png" if path else IMAGES_DIR / "grid.png"
    g.save(str(output))

if __name__ == '__main__':
    main()

def test_grid(tmp_path):
    main(tmp_path)
