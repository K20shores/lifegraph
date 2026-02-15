from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date
from pathlib import Path

IMAGES_DIR = Path(__file__).parent / "images"

def main(path=None):
    birthday = date(1990, 11, 1)
    image_path = str(Path(__file__).parent / "couple.jpg")
    g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

    g.add_title("Time is Not Equal to Money")
    g.show_max_age_label()

    g.add_image(image_path, alpha=0.5)

    output = Path(path) / "grid_add_image.png" if path else IMAGES_DIR / "grid_add_image.png"
    g.save(str(output))

if __name__ == '__main__':
    main()

def test_grid_add_image(tmp_path):
    main(tmp_path)
