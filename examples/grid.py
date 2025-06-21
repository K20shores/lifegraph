from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

def main(path=None):
    birthday = date(1990, 11, 1)
    g = Lifegraph(birthday, dpi=300, size=Papersize.A4, axes_rect=[.1, .1, .8, .8])
    if path:
        g.save(f"{path}/grid.png")
    else:
        g.save("images/grid.png")

if __name__ == '__main__':
    main()

def test_grid(tmp_path):
    main(tmp_path)
