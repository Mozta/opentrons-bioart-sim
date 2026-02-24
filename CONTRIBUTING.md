# Contributing to Opentrons Bio-Art Simulator

Thank you for your interest in contributing!

## Getting Started

1. **Fork** this repository
2. **Clone** your fork locally
3. Create a **virtual environment** and install dev dependencies:

```bash
python -m venv venv
source venv/bin/activate     # macOS/Linux
pip install -e ".[dev]"
```

4. Create a feature **branch**:

```bash
git checkout -b my-feature
```

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Linting

```bash
ruff check src/ tests/
```

### Running a Protocol

```bash
opentrons-bioart-sim examples/octocat.py --save output.png
```

## Submitting Changes

1. Commit your changes with clear messages
2. Push to your fork
3. Open a **Pull Request** against `main`
4. Describe what your change does and why

## Ideas for Contributions

- 🎨 Add more example protocols
- 🧪 Improve test coverage
- 🌐 Add translations to the README
- 📊 Add new visualization backgrounds (e.g., UV light simulation)
- 🔧 Support additional pipette types
- 📝 Improve documentation

## Code of Conduct

Be respectful, inclusive, and constructive. We're all here to learn and create bio-art!
