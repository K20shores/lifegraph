from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date
from pathlib import Path

IMAGES_DIR = Path(__file__).parent / "images"

def main(path=None):
    birthday = date(1990, 11, 1)
    g = Lifegraph(birthday, dpi=300, size=Papersize.A4)
    g.add_title("Time is Not Equal to Money")
    output = Path(path) / "grid_with_title.png" if path else IMAGES_DIR / "grid_with_title.png"
    g.save(str(output))

if __name__ == '__main__':
    main()

def test_grid_with_title(tmp_path):
    main(tmp_path)
