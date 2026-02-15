from lifegraph.lifegraph import Lifegraph, Papersize, Side
from datetime import date
from pathlib import Path

IMAGES_DIR = Path(__file__).parent / "images"

def main(path=None):
    birthday = date(1990, 11, 1)
    g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

    g.add_title("Time is Not Equal to Money")
    g.show_max_age_label()

    # a random color will be chosen if you don't provide one
    g.add_life_event('My first paycheck', date(2006, 8, 23))

    # colors can be added as hex strings
    # and you can hint at which side you want the text on
    g.add_life_event('Graduated\nhighschool', date(2008, 6, 2), color="#00FF00", side=Side.LEFT)

    # or RGB
    g.add_life_event('First car purchased', date(2010, 7, 14), color = (1, 0, 0))

    output = Path(path) / "grid_life_event.png" if path else IMAGES_DIR / "grid_life_event.png"
    g.save(str(output))

if __name__ == '__main__':
    main()

def test_grid_life_event(tmp_path):
    main(tmp_path)
