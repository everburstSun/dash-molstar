# dash-molstar Changelog

## [1.2.1] - 2024-11-09
### Changed
- Making named params as a classmethod

## [1.2.0] - 2024-09-23
### Added
- Loading trajectories now supported
- Loading structures without default representation
- Fully customizable component representations
- Import and export representation configurations as JSON file
- Showing assembly when loading structures
- Drawing spheres on the stage
- Allowing transparency on shapes

## [1.1.2] - 2024-02-22
### Bug fixes
- Fixed the problem when loading multiple structures with components.

## [1.1.1] - 2023-09-30
### Bug fixes
- Fixed the problem when selected only one target, the plugin would fail.

## [1.1.0] - 2023-09-16
### Added
- Adding custom html class names for the molstar container
- Drawing bounding boxes
- Selecting residues with insertion code
- Selecting residues and chains using the authentic numbers or names when working with CIF files
- Loading structures from remote urls

### Bug fixes
- Fixed the problem when the user toggles full-screen mode, molstar would be possibly hidden by other elements.

## [1.0.1] - 2023-05-09
### Bug fixes
- Fixed installation issue with pip

## [1.0.0] - 2023-05-04
### Initial release