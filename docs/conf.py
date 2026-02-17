"""Sphinx configuration for lifegraph documentation."""

import os
import sys

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, os.path.abspath(".."))

import lifegraph

# -- Project information -----------------------------------------------------
project = "lifegraph"
copyright = "2024, Kyle Shores"
author = "Kyle Shores"
version = lifegraph.__version__
release = lifegraph.__version__

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_gallery.gen_gallery",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Napoleon settings -------------------------------------------------------
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_use_param = True
napoleon_use_rtype = True

# -- Autodoc settings --------------------------------------------------------
autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
}

# -- Intersphinx mapping -----------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "numpy": ("https://numpy.org/doc/stable", None),
}

# -- Sphinx-Gallery configuration --------------------------------------------
from sphinx_gallery.sorting import ExplicitOrder, FileNameSortKey

sphinx_gallery_conf = {
    "examples_dirs": ["../examples"],
    "gallery_dirs": ["auto_examples"],
    "filename_pattern": r"/plot_",
    "ignore_pattern": r"(all_sizes|__init__)\.py",
    "subsection_order": ExplicitOrder(
        [
            "../examples/getting_started",
            "../examples/events_and_eras",
            "../examples/customization",
            "../examples/advanced",
            "../examples/complete_example",
        ]
    ),
    "within_subsection_order": FileNameSortKey,
    "thumbnail_size": (400, 400),
    "show_signature": False,
}

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"
html_title = "lifegraph"
html_static_path = ["_static"]

html_theme_options = {
    "source_repository": "https://github.com/kyleshores/Life-Graph",
    "source_branch": "main",
    "source_directory": "docs/",
}
