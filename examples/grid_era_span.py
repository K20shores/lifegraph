from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

def main(path=None):
    birthday = date(1990, 11, 1)
    g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

    g.add_title("Time is Not Equal to Money")
    g.show_max_age_label()

    # random color will be used
    g.add_era_span('That one thing\nI did as a kid', date(2000, 3, 4), date(2005, 8, 22))

    # you can also choose the color
    g.add_era_span('Running for city\ncouncil', date(2019, 12, 10), date(2020, 11, 5), color="#4423fe")

    if path:
        g.save(f"{path}/grid_era_span.png")
    else:
        g.save("images/grid_era_span.png")

if __name__ == '__main__':
    main()

def test_grid_era_span(tmp_path):
    main(tmp_path)
