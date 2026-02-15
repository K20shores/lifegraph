from lifegraph.lifegraph import Lifegraph, Papersize, Point, Side
from datetime import date, datetime
from pathlib import Path

IMAGES_DIR = Path(__file__).parent / "images"

def main(path=None):
    birthday = date(1995, 11, 20)
    g = Lifegraph(birthday, dpi=300, size=Papersize.Letter, label_space_epsilon=1)

    g.add_life_event('Won an award', date(2013, 11, 20), '#014421')
    g.add_life_event('Hiked the Rocky Mountains', date(2014, 2, 14), '#DC143C', hint=(25, -3))
    g.add_life_event('Ran first marathon', date(2017, 9, 11), '#990000')
    g.add_life_event('Built a canoe', date(2018, 12, 8), '#87CEFA')
    g.add_life_event('Started working at\nEcosia', date(2019, 1, 7), '#00008B')

    now = datetime.now(tz=None)
    g.add_life_event('Today', date(now.year, now.month, now.day), (0.75, 0, 0.75))

    g.add_era("Elementary School", date(2001, 8, 24), date(2007, 6, 5), 'r')
    g.add_era("Intermediate School", date(2007, 8, 24), date(2008, 6, 5), '#00838f')
    g.add_era("Middle School", date(2008, 8, 24), date(2010, 6, 5), 'b')
    g.add_era("High School", date(2010, 8, 24), date(2014, 6, 5), '#00838f')
    g.add_era("College", date(2014, 9, 1), date(2018, 12, 14), (80/255, 0, 0), side=Side.LEFT)

    g.add_era_span("Longest vacation ever", date(2016, 8, 22), date(2016, 12, 16), '#D2691E', hint=Point(53, 28))

    g.add_title("The life of Someone")

    g.show_max_age_label()

    output = Path(path) / "alife.png" if path else IMAGES_DIR / "alife.png"
    g.save(str(output))

if __name__ == "__main__":
    main("images")

def test_alife(tmp_path):
    main(tmp_path)
