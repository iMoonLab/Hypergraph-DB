# Contributing to Hypergraph-DB

Thank you for your interest in contributing to Hypergraph-DB! We welcome contributions from the community and are grateful for your help in making this project better.

##  Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## 🤝 How to Contribute

There are many ways to contribute to Hypergraph-DB:

- 🐛 **Report bugs** - Help us identify and fix issues
- 💡 **Suggest features** - Share ideas for new functionality
- 📖 **Improve documentation** - Help make our docs clearer and more comprehensive
- 🔧 **Submit code** - Fix bugs or implement new features
- 🧪 **Write tests** - Help improve our test coverage
- 🌐 **Translate** - Help make the project accessible in more languages

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Git

### Setting up the Development Environment

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/your-username/Hypergraph-DB.git
   cd Hypergraph-DB
   ```

2. **Install dependencies**:
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -e ".[dev]"
   ```

3. **Run tests to ensure everything works**:
   ```bash
   # Using uv
   uv run pytest
   
   # Or using pip
   pytest
   ```

4. **Set up pre-commit hooks** (optional but recommended):
   ```bash
   uv run pre-commit install
   ```

## 📤 Submitting Changes

### Pull Request Process

1. **Create a new branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our [style guidelines](#style-guidelines)

3. **Add tests** for new functionality

4. **Update documentation** if needed

5. **Run tests and ensure they pass**:
   ```bash
   uv run pytest
   ```

6. **Run type checking**:
   ```bash
   uv run mypy hyperdb
   ```

7. **Format your code**:
   ```bash
   uv run black hyperdb tests
   uv run isort hyperdb tests
   ```

8. **Commit your changes** with a clear message:
   ```bash
   git commit -m "feat: add new hypergraph algorithm"
   ```

9. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

10. **Create a Pull Request** on GitHub

### Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - A new feature
- `fix:` - A bug fix
- `docs:` - Documentation only changes
- `style:` - Changes that do not affect the meaning of the code
- `refactor:` - A code change that neither fixes a bug nor adds a feature
- `test:` - Adding missing tests or correcting existing tests
- `chore:` - Changes to the build process or auxiliary tools

## 🐛 Reporting Issues

When reporting issues, please include:

1. **Bug Description**: Clear description of the problem
2. **Environment**: Python version, OS, package version
3. **Reproduction Steps**: Minimal code example that reproduces the issue
4. **Expected Behavior**: What you expected to happen
5. **Actual Behavior**: What actually happened
6. **Stack Trace**: If applicable, include the full error message

Please provide as much detail as possible when reporting issues.

## 📖 Documentation

We use [MkDocs](https://www.mkdocs.org/) with the Material theme for documentation:

### Building Documentation Locally

```bash
# Install documentation dependencies
uv sync --extra docs

# Serve documentation locally
uv run mkdocs serve

# Build documentation
uv run mkdocs build
```

### Documentation Guidelines

- Write clear, concise explanations
- Include code examples for new features
- Update both English and Chinese versions when possible
- Use proper Markdown formatting
- Add diagrams or images when helpful

## 🧪 Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=hyperdb

# Run specific test file
uv run pytest tests/test_hypergraph.py

# Run tests matching a pattern
uv run pytest -k "test_add_vertex"
```

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Follow the existing test structure
- Include edge cases and error conditions
- Aim for high test coverage

### Test Structure

```python
def test_feature_name():
    """Test description."""
    # Arrange
    hg = HypergraphDB()
    
    # Act
    result = hg.some_method()
    
    # Assert
    assert result == expected_value
```

## 📝 Style Guidelines

### Python Code Style

We use the following tools to maintain code quality:

- **[Black](https://black.readthedocs.io/)** - Code formatting
- **[isort](https://pycqa.github.io/isort/)** - Import sorting
- **[mypy](https://mypy.readthedocs.io/)** - Type checking
- **[flake8](https://flake8.pycqa.github.io/)** - Linting

### Code Guidelines

1. **Type Hints**: Use type hints for all public APIs
2. **Docstrings**: Follow [NumPy docstring style](https://numpydoc.readthedocs.io/en/latest/format.html)
3. **Variable Names**: Use descriptive names (`vertex_id` not `vid`)
4. **Function Names**: Use verbs for functions (`add_vertex` not `vertex_add`)
5. **Class Names**: Use PascalCase (`HypergraphDB`)
6. **Constants**: Use UPPER_SNAKE_CASE (`MAX_VERTICES`)

### Example Docstring

```python
def add_vertex(self, vertex_id: Hashable, attributes: Optional[Dict[str, Any]] = None) -> None:
    """Add a vertex to the hypergraph.

    Parameters
    ----------
    vertex_id : Hashable
        Unique identifier for the vertex.
    attributes : dict, optional
        Dictionary of vertex attributes, by default None.

    Raises
    ------
    ValueError
        If vertex_id already exists in the hypergraph.

    Examples
    --------
    >>> hg = HypergraphDB()
    >>> hg.add_vertex(1, {"name": "Alice", "age": 30})
    """
```

## 🏷️ Release Process

Releases are handled by maintainers and follow semantic versioning:

- **Major** (X.0.0): Breaking changes
- **Minor** (0.X.0): New features, backward compatible
- **Patch** (0.0.X): Bug fixes, backward compatible

## 🙋 Getting Help

If you need help or have questions:

1. Check the [documentation](https://imoonlab.github.io/Hypergraph-DB/)
2. Search [existing issues](https://github.com/iMoonLab/Hypergraph-DB/issues)
3. Create a [new discussion](https://github.com/iMoonLab/Hypergraph-DB/discussions)
4. Join our community channels (if available)

## 📄 License

By contributing to Hypergraph-DB, you agree that your contributions will be licensed under the Apache License 2.0.

---

Thank you for contributing to Hypergraph-DB! 🚀
