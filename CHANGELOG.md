# Changelog

All notable changes to this project will be documented in this file.

The format follows the principles of
Keep a Changelog.

Semantic Versioning is adopted.

---

## [Unreleased]

### Added

- CSV Dataset Importer for file-path and stream sources
- CSV validation for the official dataset format
- Mapping from external contest data to DrawId, DrawDate, and Combination
- Validation of Jolly and Superstar fields with discard semantics at the domain boundary
- Atomic construction of imported Dataset instances
- Dedicated CSV importer exception hierarchy

### Engineering

- C2 Import Tools completed and certified
- CSV Dataset Importer test suite completed

---

## [0.1.0-alpha1]

Initial engineering release.

### Added

- Repository layout
- Kernel foundation
- Number Value Object
- Combination Value Object
- Initial documentation
- Initial test suite
- Draw Aggregate Root
- DrawId Value Object
- DrawDate Value Object
- Domain Layer completed
- Domain documentation
- Domain specifications
- Domain test suite

### Changed

- Kernel public API updated
- Domain exports completed

### Engineering

- Builder Layer completed (M1.3)
- Domain Layer completed (M1.4)
- Domain Consistency Review (DCR-002) completed
- Foundation Layer frozen
- Collections Layer frozen
- Builder Layer frozen
- Domain Layer frozen
