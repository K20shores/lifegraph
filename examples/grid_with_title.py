from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

def main(path=None):
    birthday = date(1990, 11, 1)
    g = Lifegraph(birthday, dpi=300, size=Papersize.A4)
    g.add_title("Time is Not Equal to Money")
    if path:
        g.save(f"{path}/grid_with_title.png")
    else:
        g.save("images/grid_with_title.png")

if __name__ == '__main__':
    main()

def test_grid_with_title(tmp_path):
    main(tmp_path)
