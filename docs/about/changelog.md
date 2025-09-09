# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-09-09

### Added
- 📖 Chinese documentation support
- 🌐 Internationalization (i18n) configuration
- 📚 Comprehensive API documentation
- 🎨 Improved visualization interface
- Migrated documentation from Sphinx to MkDocs
- Advanced usage patterns and tutorials

### Changed
- 🔧 Better error handling
- ⚡ Performance optimizations
- 📝 More detailed code examples
- 🧪 Enhanced test coverage
- Updated project structure for modern Python development
- Migrated from Poetry to uv for dependency management
- Enhanced development workflow with automated scripts

### Fixed
- 🐛 Fixed visualization rendering issues
- 📖 Documentation and code consistency fixes
- 🔗 Fixed internal link issues

## [0.1.2] - 2024-12-22

### Fixed
- 🐛 Fixed bugs in `remove_e()` function
- 📖 Updated README documentation

## [0.1.1] - 2024-12-16

### Added
- 🧪 More comprehensive test suite
- 📊 Dedicated stress tests to ensure system stability and performance

### Changed
- ⚡ **Major Performance Improvement**: 100x speed boost for hypergraph construction and querying
  - Constructing a hypergraph with 10,000 nodes and performing 40,000 vertex and hyperedge queries
  - v0.1.0 took 90 seconds, v0.1.1 only takes 0.05 seconds
- Improved API design and consistency
- Better documentation and examples

## [0.1.0] - 2024-12-16

### Added
- 🎉 Initial release of Hypergraph-DB
- 📊 Core hypergraph data structure implementation
- 🎨 Web visualization interface
- 📖 Basic documentation and API reference
- 🧪 Basic test suite

### Core Features
- 🏗️ `Hypergraph` core class
- 🔗 Hyperedge operations
- 📊 Hypervertex operations
- 📈 Basic graph algorithms
- 🎯 Neighbor query functionality

### Visualization Features
- 🌐 Web-based hypergraph visualization
- 🎨 Interactive hypergraph display
- 📱 Responsive design
- 🎛️ Customizable visual styles

### API Features
- ➕ `add_hyperedge()` - Add hyperedge
- ➕ `add_hypervertex()` - Add hypervertex
- 🗑️ `remove_hyperedge()` - Remove hyperedge
- 🗑️ `remove_hypervertex()` - Remove hypervertex
- 📊 `degree_v()` - Calculate hypervertex degree
- 📊 `degree_e()` - Calculate hyperedge degree
- 🔍 `nbr_v_of_e()` - Query adjacent hypervertices of hyperedge
- 🔍 `nbr_e_of_v()` - Query adjacent hyperedges of hypervertex
- 🎨 `draw()` - Visualize hypergraph

[Unreleased]: https://github.com/iMoonLab/Hypergraph-DB/compare/v0.1.3...HEAD
[0.1.3]: https://github.com/iMoonLab/Hypergraph-DB/compare/v0.1.3...v0.1.3
[0.1.2]: https://github.com/iMoonLab/Hypergraph-DB/compare/v0.1.0...v0.1.2
[0.1.1]: https://github.com/iMoonLab/Hypergraph-DB/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/iMoonLab/Hypergraph-DB/releases/tag/v0.1.0
