"""Run every gallery example script to make sure it still works."""

import runpy
from pathlib import Path

import matplotlib.pyplot as plt
import pytest

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"

PLOT_SCRIPTS = sorted(EXAMPLES_DIR.rglob("plot_*.py"))


@pytest.fixture(autouse=True)
def _close_figures():
    """Close all matplotlib figures after every test."""
    yield
    plt.close("all")


@pytest.mark.parametrize(
    "script",
    PLOT_SCRIPTS,
    ids=[str(s.relative_to(EXAMPLES_DIR)) for s in PLOT_SCRIPTS],
)
def test_example_script(script, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(str(script), run_name="__main__")


def test_all_sizes(tmp_path):
    from examples.all_sizes import main

    main(tmp_path)
