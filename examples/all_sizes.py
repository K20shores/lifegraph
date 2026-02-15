from lifegraph.lifegraph import Lifegraph, Papersize, random_color, Point, Side
from datetime import date, datetime, timedelta
from pathlib import Path

IMAGES_DIR = Path(__file__).parent / "images"

def main(path=None):
    birthday = date(1990, 11, 1)
    image_path = str(Path(__file__).parent / "couple.jpg")

    for sz in Papersize:
        print(f"{sz}")
        g = Lifegraph(birthday, dpi=100, size=sz, label_space_epsilon=1)

        g.add_life_event('Married', date(2010, 2, 14), '#DC143C')
        g.add_life_event('Five Years\nTogether', date(2015, 2, 14), '#DC143C')

        g.add_watermark("A Person")

        g.add_era("Elementary School", date(1996, 8, 24), date(2002, 6, 5), 'r')
        g.add_era("Intermediate School", date(2002, 8, 24), date(2003, 6, 5), '#00838f')
        g.add_era("Middle School", date(2003, 8, 24), date(2005, 6, 5), 'b')
        g.add_era("High School", date(2005, 8, 24), date(2009, 6, 5), '#00838f')
        g.add_era("College", date(2009, 9, 1), date(2013, 12, 14), (80/255, 0, 0), side=Side.LEFT)

        g.add_era_span("Pregnant with\nBilbo Bagginses", date(2016, 1, 22), date(2016, 10, 16), '#D2691E', hint=Point(54, 28))

        g.add_title("Our Life, Together")

        g.add_image(image_path, alpha=0.3)

        g.show_max_age_label()

        output = Path(path) / f"lifegraph_{sz.name}.png" if path else IMAGES_DIR / f"lifegraph_{sz.name}.png"
        g.save(str(output))
        g.close()

if __name__ == '__main__':
    main()

def test_all_sizes(tmp_path):
    main(tmp_path)
