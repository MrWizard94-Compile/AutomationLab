# References — 1.16.5 → 1.20.1 Forge porting knowledge base

This directory is the **cognition seed** for the [[Smart Library]] node: the verified map of how
Astral Sorcery's `1.16.5` (Forge 36.2.22, Java 8, MCP mappings) source maps onto the target
`1.20.1` (Forge 47.3.0, Java 17, official/Mojmap mappings) build in
`C:\WPAI\Gaming\Minecraft\Mods-1.20.1-Forge\Astral_Sorcery_Port`.

## How to use it

These notes are a **conceptual map plus a method**, not a frozen API dump. Exact method
signatures drift between Forge builds and rot fast — so the rule is:

> **The map tells you *what* transform to apply. The live MDK and the running
> `AST_LSP` compile gate tell you the *exact* signature.** Never hand-copy a signature from
> memory into the port; resolve it against the deobfuscated sources the project already has
> (ForgeGradle decompiles them) and let the compile/Checkstyle/SpotBugs rungs confirm it.

This keeps the system honest: the references accelerate the [[Executor]], but the deterministic
[[Verification Ladder]] — not this document — is the source of truth that gates acceptance.

## ⚠️ The single most expensive misconception

**This port targets 1.20.1, NOT 1.20.5+ / NeoForge.** Therefore:

- **NBT stays.** `CompoundTag` is alive and well. **DataComponents do not exist in 1.20.1.**
- **Forge capabilities stay.** `LazyOptional` + `ICapabilityProvider` + `RegisterCapabilitiesEvent`
  are the model. The capability *removal* is 1.20.5+/NeoForge.
- **`SimpleChannel` networking stays.** The custom-payload `StreamCodec` system is 1.20.4+/NeoForge.

Over-porting any of these three to the newer idiom is the classic way to wreck a 1.20.1 codebase.
The repo CLAUDE (§4) forbids it explicitly.

## Index

- [`forge-1.16.5-to-1.20.1-deltas.md`](forge-1.16.5-to-1.20.1-deltas.md) — master rename/registration/data table.
- [`rendering-and-gui.md`](rendering-and-gui.md) — `PoseStack`, `GuiGraphics`, `BlockEntityRenderer`, shader-based draws (highest visual-parity risk).
- [`worldgen-1.16-to-1.20.md`](worldgen-1.16-to-1.20.md) — configured/placed features + BiomeModifiers (largest single delta).
- [`optional-integrations.md`](optional-integrations.md) — JEI, Curios, ObserverLib, Patchouli, Botania, CraftTweaker, Tombstone.
- [`toolchain-and-gates.md`](toolchain-and-gates.md) — the exact gradle tasks the [[Verification Ladder]] runs.
