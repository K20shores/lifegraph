"""
Example demonstrating how to use Lifegraph with a provided matplotlib axes instance.

This example shows how to:
1. Create a matplotlib figure and axes
2. Pass the axes to Lifegraph
3. Use multiple lifegraphs on different subplots
"""
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date
from pathlib import Path
import matplotlib.pyplot as plt

IMAGES_DIR = Path(__file__).parent / "images"


def single_axes_example(path=None):
    """Example of using Lifegraph with a single provided axes"""
    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(10, 8))

    # Create Lifegraph with the provided axes
    birthday = date(1990, 11, 1)
    g = Lifegraph(birthday, max_age=50, ax=ax)

    # Add some life events
    g.add_life_event('First Job', date(2012, 6, 1), color='#00FF00')
    g.add_life_event('Got Married', date(2015, 8, 15), color='#FF1493')
    g.add_life_event('Started PhD', date(2018, 9, 1), color='#1E90FF')

    g.add_title("My Life (Single Axes Example)")

    # Since we provided the axes, we trigger drawing explicitly
    g.draw()

    # Since we provided the axes, we control the figure lifecycle
    output = Path(path) / "provided_axes_single.png" if path else IMAGES_DIR / "provided_axes_single.png"
    fig.savefig(str(output), dpi=300, bbox_inches='tight')

    plt.close(fig)


def multiple_subplots_example(path=None):
    """Example of using Lifegraph with multiple subplots"""
    # Create a figure with two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Create two different life graphs
    person1_birthday = date(1985, 3, 15)
    person2_birthday = date(1992, 7, 20)

    g1 = Lifegraph(person1_birthday, max_age=50, ax=ax1)
    g2 = Lifegraph(person2_birthday, max_age=50, ax=ax2)

    # Add events for person 1
    g1.add_life_event('Graduated College', date(2007, 5, 20), color='#FFD700')
    g1.add_life_event('First Child', date(2012, 3, 10), color='#FF69B4')
    g1.add_title("Person 1's Life")

    # Add events for person 2
    g2.add_life_event('Started Career', date(2014, 8, 1), color='#32CD32')
    g2.add_life_event('Bought House', date(2019, 11, 5), color='#8B4513')
    g2.add_title("Person 2's Life")

    # Trigger drawing on both subplots
    g1.draw()
    g2.draw()

    # Adjust layout and save
    plt.tight_layout()

    output = Path(path) / "provided_axes_multiple.png" if path else IMAGES_DIR / "provided_axes_multiple.png"
    fig.savefig(str(output), dpi=300, bbox_inches='tight')

    plt.close(fig)


def mixed_plot_example(path=None):
    """Example mixing Lifegraph with other matplotlib plots"""
    # Create a figure with multiple subplots of different types
    fig = plt.figure(figsize=(16, 10))

    # Life graph in the top subplot
    ax1 = fig.add_subplot(2, 1, 1)
    birthday = date(1988, 5, 10)
    g = Lifegraph(birthday, max_age=50, ax=ax1)
    g.add_life_event('Career Change', date(2015, 1, 1), color='#FF6347')
    g.add_title("Life Timeline")

    # Trigger drawing on the lifegraph axes
    g.draw()

    # Regular matplotlib plot in the bottom subplot
    ax2 = fig.add_subplot(2, 1, 2)
    years = [2010, 2012, 2014, 2016, 2018, 2020]
    happiness = [6, 7, 5, 8, 9, 8]
    ax2.plot(years, happiness, marker='o', linewidth=2, color='#4169E1')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Happiness Level')
    ax2.set_title('Happiness Over Time')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    output = Path(path) / "provided_axes_mixed.png" if path else IMAGES_DIR / "provided_axes_mixed.png"
    fig.savefig(str(output), dpi=300, bbox_inches='tight')

    plt.close(fig)


def main(path=None):
    """Run all examples"""
    print("Creating single axes example...")
    single_axes_example(path)

    print("Creating multiple subplots example...")
    multiple_subplots_example(path)

    print("Creating mixed plot example...")
    mixed_plot_example(path)

    print("Examples created successfully!")


if __name__ == '__main__':
    main()
