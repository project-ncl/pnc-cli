# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [Unreleased]
### Changed
- Fixed spelling of the long '--suffix' option to the make-mead command

### Added
- [NCL-4244] build and build_set commands now supports --rebuild-mode argument. The --force-rebuild (-f) argument is now being deprecated in these commands.

### Fixed
- Fixed anonymous usage

## [1.4.1] - 2018-10-01
### Fixed
- Fixed error handling in make-mead command
- Fixed code indentation

## [1.4.0] - 2018-09-27
### Added
- Added new argument --clean-group to make-mead command for cleaning old Build Configurations in Build Group Config
- Added cancel-running-build command
- Added new argument --get-revision to update-build-configuration command to get the revision of the updated Build Configuration
- Added new argument --rev to build command to allow selection specific revision of Build Configuration to build
- Added new argument --id-revisions to build-set command to allow selection specific revision of Build Configurations from the Build Group Config to build 

### Changed
- Fixed and updated query-by-attribute command
- Changed create-repository-configuration command to automatically recognize internal/external repository
- Argument revision_id is now positional and required in get-revision-of-build-configuration command
- The user token is refreshed before running command, allowing to successfuly finish long running builds. 
- Updated swagger client-code generator to version 2.2.3 
- ApiExceptions are now output to stderr instead of stdout

### Fixed
- Fixed parsing of get-environment command output

## [1.3.6] - 2018-09-18
### Fixed
- fixed update-repository-configuration command

## [1.3.5] - 2018-08-07
### Fixed
- [NCL-4033] fixed pageination in list-dependencies command

## [1.3.4] - 2018-08-07
### Fixed
- [NCL-4016] fixed list-build-configurations-for-product command

## [1.3.3] - 2018-08-07
### Fixed
- [NCL-4006] fixed wrong formating in geting build-set
- [NCL-3997] fixed broken git url validation
- fixed get-log-for-record command

## [1.3.2] - 2018-07-31
### Fixed
- [NCL-3947] fixed inifite recurion in list-build-set-records
- [NCL-4004] fixed unicode sanitization
- [NCL-3997] fixed git url validation

## [1.3.1] - 2018-07-30
### Fixed
- [NCL-3998] fixed rsql and pagination in list-projects command

## [1.3.0] - 2018-06-26
### Added
- Added support for temporary builds
- Add Brew push commands
- Added command to genereate list of built artifact
- make-mead command now creates Product Version if it doesn't exists

### Changed
- Replaced prints with logging and added option to specify log level
- Improved test coverage
- Rework auth so credentials are requested lazily

### Removed
- Removed some environment commands that actually don't exists in PNC
- Removed license commands as licenses are not supported in PNC
- Removed broken duplicate list-artifacts command (use list-built-artifacts instead)

### Fixed
- [NCL-4004] Fix unicode sanitization in swagger client
- [NCL-3947] Fix inifite recurion in list-build-set-records
- [NCL-3997] Fix git url validation
- [NCL-3998] Fix list-projects with rsql returns everything
- [NCL-3878] Fix ProductMilestoneRest not iterable
- [NCL-3828] Fix wrong formating of json
- [NCL-3710] Fix return format of build config commands
- [NCL-3498] fix 0 return value when makemead fails
- Fix three bugs in the `pnc make-mead` command
- Fix reutrn type of BuildConfigurationSets.build
- Fix crash in get-product command when the product doesn't exist

