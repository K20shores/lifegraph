# Contributing

Thank you for your interest in contributing to lifegraph!

## Creating an Issue or Feature Request

If you find a bug, please [open an issue](https://github.com/kyleshores/Life-Graph/issues)
with a description of what happened and a minimal code snippet that reproduces
it. Even if you plan to submit a pull request, please link it to an issue.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/kyleshores/Life-Graph.git
cd Life-Graph

# Create a virtual environment and install dev dependencies
pip install -e ".[dev,docs]"

# Run the test suite
python -m pytest -v

# Build the documentation locally
cd docs && sphinx-build -b html . _build/html
```

## Creating a Pull Request

1. Fork the repository and create a branch from `main`.
2. Add or update tests for any changed behaviour.
3. Make sure `python -m pytest` passes.
4. Open a pull request -- it will be reviewed and merged once any feedback is
   addressed.
