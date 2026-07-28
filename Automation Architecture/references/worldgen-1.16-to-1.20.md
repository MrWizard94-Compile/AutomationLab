# Worldgen — 1.16.5 → 1.20.1

**Largest single delta in the port.** Worldgen was rewritten between 1.16 and 1.18 (and tuned
again through 1.20). It went from Java-registered, event-injected features to a **data-driven,
registry-keyed** system. Expect this phase to produce multiple [[Escalation]]s.

## What Astral Sorcery generates

Rock Crystal Ore, marble/aquamarine deposits, sky/light-related structures, floating crystals —
i.e. ore-style features plus a few bespoke placements. Each becomes a configured + placed feature
plus a biome injection.

## The new model

1. **`ConfiguredFeature<FC, F>`** — *what* to place (e.g. `Feature.ORE` with an `OreConfiguration`
   of target block-states + vein size). Now defined as **JSON datapack entries** under
   `data/<ns>/worldgen/configured_feature/…`, generated via datagen.
2. **`PlacedFeature`** — *where/how often* to place it, via a list of **`PlacementModifier`s**
   (`CountPlacement`, `RarityFilter`, `InSquarePlacement`, `HeightRangePlacement`,
   `BiomeFilter`…). This **replaces** the 1.16 `Placement`/decorator + `ConfiguredPlacement`
   system. JSON under `data/<ns>/worldgen/placed_feature/…`.
3. **Biome injection** — 1.16 added features in `BiomeLoadingEvent`. In 1.20.1 Forge use a
   **`BiomeModifier`** (data-driven JSON, type `forge:add_features`) under
   `data/<ns>/forge/biome_modifier/…`, generated via a `BiomeModifier` datagen provider, selecting
   biomes by tag and the generation `Decoration` step.

## Registry plumbing

- Worldgen objects live in **datapack registries** keyed by `ResourceKey` (`Registries.CONFIGURED_FEATURE`,
  `Registries.PLACED_FEATURE`, `Registries.BIOME_MODIFIER`). Bootstrap them with a
  `RegistrySetBuilder` in datagen (`DatapackBuiltinEntriesProvider`).
- Custom `Feature<FC>` subclasses (if AS has bespoke generation logic) are still registered in code
  via `DeferredRegister(ForgeRegistries.FEATURES)`; only their *configuration/placement* moves to
  JSON.

## Strategy for the [[Executor]]

Port the **custom `Feature` classes first** (code, gated by compile), then generate the
configured/placed/biome-modifier **JSON via datagen** (gated by `runData --validate`), then verify
actual placement with a **`@GameTest`** that loads a chunk and asserts the ore/structure appears.
Do not hand-write the worldgen JSON — let the Asset Converter route it through datagen so the
`--validate` rung proves every `ResourceLocation` resolves.
