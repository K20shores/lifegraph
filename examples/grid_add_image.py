from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date
import os

def main(path=None):
    birthday = date(1990, 11, 1)
    image_path = os.path.join(os.path.dirname(__file__), "couple.jpg")
    g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

    g.add_title("Time is Not Equal to Money")
    g.show_max_age_label()

    g.add_image(image_path, alpha=0.5)

    if path:
        g.save(f"{path}/grid_add_image.png")
    else:
        g.save("images/grid_add_image.png")

if __name__ == '__main__':
    main()

def test_grid_add_image(tmp_path):
    main(tmp_path)
