# Changelog

## Version 0.4.0 (February 16, 2026)

Features: 

- Bugs by @K20shores in https://github.com/K20shores/lifegraph/pull/36
- Add JSON/YAML import/export for lifegraph configurations by @K20shores in https://github.com/K20shores/lifegraph/pull/37
- Range by @K20shores in https://github.com/K20shores/lifegraph/pull/38
- Fix leap year bug in date-to-grid-position calculation by @K20shores in https://github.com/K20shores/lifegraph/pull/39
- Replace tutorial with image-forward gallery by @K20shores in https://github.com/K20shores/lifegraph/pull/40


[Full Changelog](https://github.com/K20shores/lifegraph/compare/v0.3.0...v0.4.0)


## Version 0.3.0 (February 15, 2026)

Features: 

- Rework configuration: extract mplstyle, fix axes styling and layout by @K20shores in https://github.com/K20shores/lifegraph/pull/35

[Full Changelog](https://github.com/K20shores/lifegraph/compare/v0.2.0...v0.3.0)

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
