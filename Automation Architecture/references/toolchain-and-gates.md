# Toolchain & the gate commands

The exact gradle tasks the [[Verification Ladder]] ([[AST_LSP]]) invokes, all already configured
in `C:\WPAI\Gaming\Minecraft\Mods-1.20.1-Forge\Astral_Sorcery_Port\build.gradle` / `gradle.properties`.

## Toolchain

- **ForgeGradle** `[6.0,6.2)`, **Java 17** toolchain, **official** mappings (`mappings channel:
  'official', version: mc_version`), MC `1.20.1`, Forge `47.3.0`.
- **Mixin** `0.8.5` annotation processor; refmap `astralsorcery.refmap.json` with
  `mixin.env.remapRefMap=true` on every run; `processResources` excludes the refmap; `compileJava`
  passes `-AreobfTsrgFile`/`-AoutRefMapFile` for compile-time refmap generation.
- `-Xlint:unchecked` and `-Xlint:rawtypes` are on for every `JavaCompile`.

## The gates (rungs of the ladder)

| # | Gate | Gradle task | Hard-fail config |
|---|---|---|---|
| 1 | Compile | `compileJava` | lint flags on; any error fails |
| 2 | Checkstyle | `checkstyleMain` | `toolVersion 10.17.0`, `config/checkstyle/checkstyle.xml`, **`ignoreFailures=false`** (`checkstyleTest` disabled) |
| 3 | SpotBugs | `spotbugsMain` | `toolVersion 4.8.6`, `config/spotbugs/exclude.xml`, **`ignoreFailures=false`** (`spotbugsTest` disabled) |
| 4 | Asset/schema | `runData` | datagen run with `--all --validate --existing src/main/resources` → `src/generated/resources` |
| 5 | Unit | `test` | JUnit 5 (`useJUnitPlatform()`) |
| 6 | Runtime/GameTest | `runGameTestServer` | `forge.enabledGameTestNamespaces=astralsorcery` |
| 7 | Client-boot smoke | `runClient` | needs an auto-quit/timeout harness (window otherwise blocks) |
| 8 | Integration | `build` | runs the full assembly incl. gates 1–3 + `test` |

## Datagen review discipline

`src/generated/resources` is **intentionally excluded** from the main resource set (build.gradle
lines 86–90). The workflow: run `runData`, diff generated output against the handwritten JSON in
`src/main/resources`, then (once a provider is complete) re-enable the `srcDir` line and delete the
handwritten files datagen now replaces. The [[Asset Converter]]'s output rides this exact path so
the `--validate` rung gates every emitted file.

## Notes

- `runClient` / `runGameTestServer` download and launch Minecraft — heavy. The gate runner invokes
  them only when the work order's phase requires rungs 6–7.
- Gates 1–3 are **walls**, not advisories (zero-warning policy, global + repo CLAUDE). A single
  Checkstyle or SpotBugs hit fails the rung and emits a [[Flag]].
