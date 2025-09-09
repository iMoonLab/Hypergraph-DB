# Installation

## Stable Release

The stable version of **Hypergraph-DB** is available on PyPI. You can install it with `pip`:

```bash
pip install hypergraph-db
```

## Development Installation

For development or to get the latest features, you can install from the GitHub repository:

```bash
pip install git+https://github.com/iMoonLab/Hypergraph-DB.git
```

!!! warning "Development Version"
    The development version may be unstable and not fully tested. If you encounter any bugs, please report them in [GitHub Issues](https://github.com/iMoonLab/Hypergraph-DB/issues).

## Using uv (Recommended for Development)

For faster dependency management, we recommend using [uv](https://github.com/astral-sh/uv):

### Install uv

=== "Windows"
    ```powershell
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

=== "macOS/Linux"
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

### Clone and Setup

```bash
# Clone the repository
git clone https://github.com/iMoonLab/Hypergraph-DB.git
cd Hypergraph-DB

# Install with development dependencies
uv sync --extra dev
```

## Verify Installation

To verify that Hypergraph-DB is installed correctly:

```python
import hyperdb
print(f"Hypergraph-DB version: {hyperdb.__version__}")

# Create a simple hypergraph
hg = hyperdb.HypergraphDB()
hg.add_v(1, {"name": "test"})
print("Installation successful!")
```

## Optional Dependencies

Hypergraph-DB has minimal dependencies, but you can install optional packages for enhanced functionality:

### Visualization Dependencies

If you want to use the built-in visualization features:

```bash
# These are included in the base installation
# No additional dependencies needed for basic visualization
```

### Development Dependencies

For contributing to the project:

```bash
# Using pip
pip install hypergraph-db[dev]

# Using uv
uv sync --extra dev
```

This includes:
- `pytest` - for running tests
- `black` - for code formatting
- `isort` - for import sorting

### Documentation Dependencies

For building documentation:

```bash
# Using pip
pip install hypergraph-db[docs]

# Using uv
uv sync --extra docs
```

## Troubleshooting

### Common Issues

1. **Python Version**: Ensure you're using Python 3.10 or later
2. **Virtual Environment**: Consider using a virtual environment to avoid conflicts
3. **Permissions**: On some systems, you might need to use `pip install --user`

### Getting Help

If you encounter issues:

1. Check the [GitHub Issues](https://github.com/iMoonLab/Hypergraph-DB/issues)
2. Create a new issue with detailed information about your setup
3. Contact the maintainers at evanfeng97@qq.com
