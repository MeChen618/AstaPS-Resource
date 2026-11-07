# AstaPS Resource

Version-bound resource data used by AstaPS. Characters, weapons, monsters, scene points, abilities, and talents have received a 7.2 runtime update on the existing 7.1.0 baseline.

This update adds two characters, one weapon, 109 monster definitions, and 99 overworld points, together with their runtime dependencies. See the [update notes](docs/runtime-7.2-update.md), [manifest](docs/runtime-7.2-manifest.json), and [validation results](docs/runtime-7.2-validation.json) for coverage and pending definitions.

Place this repository's contents under the server's `resources/` directory so paths such as `resources/BinOutput/`, `resources/ExcelBinOutput/`, `resources/ScriptSceneData/`, and `resources/Server/` are available at runtime.

Reverse-engineering evidence, protocol research, sample fingerprints, reproducibility tooling, and investigation history live in [RinoPaw/Genshin-Reverse](https://github.com/RinoPaw/Genshin-Reverse). Keep this repository focused on resources consumed by the server.
