from lifegraph.lifegraph import Lifegraph, Papersize, Side
from datetime import date

def main(path=None):
    birthday = date(1990, 11, 1)
    g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

    g.add_title("Time is Not Equal to Money")
    g.show_max_age_label()

    # the default placement
    g.add_life_event('My first paycheck', date(2006, 1, 23), color='r')
    
    # a hint, in data coordinates
    g.add_life_event('My first paycheck', date(2006, 1, 23), color='r', hint=(10, -10))

    # a side
    g.add_life_event('My first paycheck', date(2006, 1, 23), color='r', side=Side.RIGHT)

    # the default placement
    g.add_era_span('Green thing', start_date=date(2010, 2, 1), end_date=date(2011, 8, 1), color='g')
    
    # a hint, in data coordinates
    g.add_era_span('Red thing', start_date=date(2012, 2, 1), end_date=date(2013, 8, 1), color='r', hint=(52, 105))

    # a side
    g.add_era_span('Blue thing', start_date=date(2014, 2, 1), end_date=date(2015, 8, 1), color='b', side=Side.LEFT)

    if path:
        g.save(f"{path}/placement.png")
    else:
        g.save("images/placement.png")

if __name__ == '__main__':
    main()

def test_placement(tmp_path):
    main(tmp_path)
