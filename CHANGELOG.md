# Changelog

## v1.1.0 (2025-11-13)

### Feat

- simple purl handling
- all create_job commands with the same cli interface
- fetch registries and store as static list
- improved parameter handling for resolve
- add parser command with job support
- integrates with claude
- dockerized mcp
- mailto header
- initial version of rate limiting
- summary
- diff
- archives
- licenses parser
- sbom parser
- dependency resolver tool
- dependency parser
- dependabot
- opencollective
- docker
- sponsors
- add commits api
- new route on advisories
- timeline
- issues api added
- packages
- packages
- autocomplete & mcp
- autocomplete
- override domain to request to
- header incl version

### Fix

- api for queue simplified
- matching of triggers
- pre-commit
- pre-commit hooks now installed with setup
- tests
- correct pipeline badge
- param errors
- packages api parameters and json output
- Command Registration Inconsistency
- display default parameters
- show base parameters in commands

### Refactor

- remove indent when returning json
- use purl paser lib
- job pattern for all
- start to fix the refactor apis
- bravado to new openapi client
- lower and upper case params fixed
- remove setup.py
- use 3rd party openapi client to avoid re-invention of wheels (sad jak face)
- improve handlers
- simplify parameters
- now its fine
- simplify further
- reduce to just 1 service and do ths right
- Complex Context Management simplified
- remove generic api call function from all commands

## [v1.0.0] - 2025-07-04

### Changes since v0.3.6

- chore(release): bump version 0.3.6 → 1.0.0
- refactor: add type hints
- refactor: simplify print_output
- refactor: cleaned up the base class containing unwanted code
- feat: ruby api added
- feat: add opencollective
- feat: add docker api
- feat: added sponsors api
- feat: issues api
- feat: commits api
- feat: timeline api
- feat: added diff api
- feat: added archives
- feat: licenses
- feat: sbom
- feat: dependency resolver
- fix: mock did some http requests
- feat: added dependency parser
- feat: advisories added
- feat: ost api
- feat: papers command added
- refactor: output less complex now
- docs: added specs for papers
- fix: make it executable again
- refactor: explicit error handling
- refactor: introrcued base class to reduce code duplication
- refactor: extract commad tests
- refactor: constants extracted
- fix: missing parameter at error log
- chore: up gitignore
- refactor: clean up the commands a bit more
- refactor: start to pull commands out
- refactor: extract commands
- refactor: extracted the print output method
- refactor: extract formatvalue method
- refactor: extract more helper methods
- docs: update CHANGELOG for v0.3.6


## [v0.3.6] - 2025-06-07

### Changes since v0.3.5

- chore(release): bump version 0.3.5 → 0.3.6
- feat: complexipy
- chore: remove leftovers
- refactor: more extracted helpers
- refactor: extract more helper methods
- refactor: extract helper methods
- feat: use bandit to do a sec check before commit or ci run pass
- chore: run lint and test on precommit hook
- docs: License information & better docs
- docs: update CHANGELOG for v0.3.5


## [v0.3.5] - 2025-03-07

### Changes since v0.3.4

- chore(release): bump version 0.3.4 → 0.3.5
- fix: add permissions to push a package to the action
- docs: update CHANGELOG for v0.3.4


## [v0.3.4] - 2025-03-07

### Changes since v0.3.3

- chore(release): bump version 0.3.3 → 0.3.4
- fix: triggered!
- docs: update CHANGELOG for v0.3.3


## [v0.3.3] - 2025-03-07

### Changes since v0.3.2

- chore(release): bump version 0.3.2 → 0.3.3
- fix: get all actions to run on release
- docs: update CHANGELOG for v0.3.2


## [v0.3.2] - 2025-03-07

### Changes since v0.3.1

- chore(release): bump version 0.3.1 → 0.3.2
- fix: run release on completion of build-test-lint
- docs: update CHANGELOG for v0.3.1


## [v0.3.1] - 2025-03-07

### Changes since v0.3.0

- chore(release): bump version 0.3.0 → 0.3.1
- fix: release pipeline conditional
- docs: update CHANGELOG for v0.3.0


## [v0.3.0] - 2025-03-07

### Changes since v0.2.1

- chore(release): bump version 0.2.1 → 0.3.0
- fix: less filtering makes the release pipeline go brrrrrr
- docs: update CHANGELOG for v0.2.1


## [v0.2.1] - 2025-03-07

### Changes since v0.2.0

- chore(release): bump version 0.2.0 → 0.2.1
- docs: update CHANGELOG for v0.2.0


## [v0.2.0] - 2025-03-07

### Changes since v0.1.2

- chore(release): bump version 0.1.2 → 0.2.0
- chore(release): bump version 0.1.1 → 0.1.2
- chore: update bump2version commit message format
- chore: switch to bump2version for release management



## v0.1.2 (2025-03-07)

### Chores

- Disable remote operations in semantic-release
  ([`f235a4c`](https://github.com/ecosyste-ms/ecosyste_ms_cli/commit/f235a4ced57cef49cf062c2fec284c1204e088f5))


## v0.1.1 (2025-03-07)

### Bug Fixes

- Added changelog
  ([`1594060`](https://github.com/ecosyste-ms/ecosyste_ms_cli/commit/1594060148bac6aaa2b4b78f08d87163c400a96d))

- Update action version for artifacts
  ([`9ab142f`](https://github.com/ecosyste-ms/ecosyste_ms_cli/commit/9ab142f06cf1509227229c180a9ac2f668e1800b))

### Chores

- .gitignore dist
  ([`75b1da4`](https://github.com/ecosyste-ms/ecosyste_ms_cli/commit/75b1da4eb67f5aff223259236f8dd1a3d8121b0e))

- Add semantic-release configuration
  ([`0b8220f`](https://github.com/ecosyste-ms/ecosyste_ms_cli/commit/0b8220fbbe90171bc685ca48a4c78873a8f1207c))

- Fix linter errors
  ([`f056174`](https://github.com/ecosyste-ms/ecosyste_ms_cli/commit/f05617445fbdbf8bfcc42f1884654cabb091e91b))

- Run pipeline on every commit
  ([`987aa56`](https://github.com/ecosyste-ms/ecosyste_ms_cli/commit/987aa56dfc68cf86f1401b1ca42a1a6b7fe1ac26))

### Features

- Prepare a release
  ([`e8cabfe`](https://github.com/ecosyste-ms/ecosyste_ms_cli/commit/e8cabfe60ea557938786f84805eb22b1e2270735))

- Release pipeline
  ([`3aba36a`](https://github.com/ecosyste-ms/ecosyste_ms_cli/commit/3aba36aa57402e159f69bd068e5f26dfb96a1911))

### Refactoring

- Release with semantic-release
  ([`2d9982a`](https://github.com/ecosyste-ms/ecosyste_ms_cli/commit/2d9982ae58b6ba7df5964684c54456742c63ff4a))


## v0.1.0 (2025-03-07)

### Chores

- Whitespaces
  ([`3d18661`](https://github.com/ecosyste-ms/ecosyste_ms_cli/commit/3d186612667eec71c12a805c0ab585a66b4a10e7))

### Features

- Add pipeline
  ([`ded6289`](https://github.com/ecosyste-ms/ecosyste_ms_cli/commit/ded6289e7a7313a9613b1730cb1ae5bb3248f9c0))

- Improved output formating
  ([`1957987`](https://github.com/ecosyste-ms/ecosyste_ms_cli/commit/1957987086b39317a4cf550391bd255990439953))

- Setup for conventional commits
  ([`b0d20e3`](https://github.com/ecosyste-ms/ecosyste_ms_cli/commit/b0d20e3025146b47fb317effd26d2cb245378ce6))
