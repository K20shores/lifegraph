# Changelog

Starting with version 0.2.0, lifegraph releases use
[semantic versioning](http://semver.org).

## Version 0.2.0 (release date TBD)

Features:

- Added support for user-provided matplotlib axes via the `ax` parameter, enabling
  subplot composition and mixing lifegraphs with other plot types.
  [#32](https://github.com/kyleshores/Life-Graph/pull/32)

- Reorganized project structure.
  [#30](https://github.com/kyleshores/Life-Graph/pull/30)

Documentation:

- Added Sphinx documentation with Furo theme, numpy-style docstrings, tutorial,
  and API reference.

## Version 0.1.0

Initial release.

- Grid of weekly squares anchored to a birthdate.
- Life events with automatic annotation placement.
- Eras with colored background shading.
- Era spans with dumbbell-shaped annotations.
- Image overlay support.
- Watermark and title support.
- Configurable paper sizes (ISO A-series, US Letter, Legal, Ledger, Tabloid, and more).
- Grid customization via matplotlib RC parameters.
