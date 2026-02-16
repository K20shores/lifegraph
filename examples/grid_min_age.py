from lifegraph.lifegraph import Lifegraph, Papersize, Side
from datetime import date
from pathlib import Path

IMAGES_DIR = Path(__file__).parent / "images"

def main(path=None):
    birthday = date(1990, 11, 1)
    g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=65, min_age=20)

    g.add_title("The Working Years")

    # Events within the visible range
    g.add_life_event("First real job", date(2013, 6, 15), color="#00008B")
    g.add_life_event("Got promoted", date(2018, 3, 1), color="#006400", side=Side.LEFT)
    g.add_life_event("Bought a house", date(2021, 9, 10), color="#8B0000")

    # Era spanning the visible range
    g.add_era("Career at Acme", date(2013, 6, 15), date(2025, 1, 1), color="#4423fe")

    # Era span
    g.add_era_span("Grad school", date(2012, 9, 1), date(2014, 5, 15), color="#D2691E")

    output = Path(path) / "grid_min_age.png" if path else IMAGES_DIR / "grid_min_age.png"
    g.save(str(output))

if __name__ == '__main__':
    main()

def test_grid_min_age(tmp_path):
    main(tmp_path)
