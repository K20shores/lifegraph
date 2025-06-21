from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

def main(path=None):
    birthday = date(1990, 11, 1)
    g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)
    g.add_title("Time is Not Equal to Money")
    g.show_max_age_label()
    if path:
        g.save(f"{path}/grid_maxage.png")
    else:
        g.save("images/grid_maxage.png")

if __name__ == '__main__':
    main()

def test_grid_maxage(tmp_path):
    main(tmp_path)
