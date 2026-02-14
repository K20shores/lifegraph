# Changelog

Starting with version 0.2.0, lifegraph releases use
[semantic versioning](http://semver.org).

## Version 0.2.0 (February 14, 2026)

Features:

- Added support for user-provided matplotlib axes via the `ax` parameter, enabling
  subplot composition and mixing lifegraphs with other plot types.
  [#32](https://github.com/K20shores/lifegraph/pull/32)

- Reorganized project structure.
  [#30](https://github.com/K20shores/lifegraph/pull/30)

Documentation:

- Added Sphinx documentation with Furo theme, numpy-style docstrings, tutorial,
  and API reference.
  [#33](https://github.com/K20shores/lifegraph/pull/33)

CI:

- Updated test matrix: dropped Python 3.9, added Python 3.14.
- Fixed PyPI URL in publish workflow.

[Full Changelog](https://github.com/K20shores/lifegraph/compare/v0.1.0...v0.2.0)

## Version 0.1.0 (June 21, 2025)

Initial release.

- Grid of weekly squares anchored to a birthdate.
- Life events with automatic annotation placement.
- Eras with colored background shading.
- Era spans with dumbbell-shaped annotations.
- Image overlay support.
- Watermark and title support.
- Configurable paper sizes (ISO A-series, US Letter, Legal, Ledger, Tabloid, and more).
- Grid customization via matplotlib RC parameters.
