# Optional integrations & the dependency wall

Under the **fail-safe + escalate** policy, every third-party integration is a [[Port Manifest]]
node. If it has a clean 1.20.1 path, port it; if not, it is `deferred` with justification + an
[[Escalation]], and **every call site is guarded** so its absence never breaks the loop.

## The established guard pattern (reuse it)

The port already does this for Curios — `AmuletEnchantmentHelper` guards all call sites via
`Mods.CURIOS.getIfPresent()`, and the integration is `compileOnly` with `mandatory=false` in
`mods.toml`. **This is the canonical pattern for every optional integration.** Compile against the
API, never hard-link at runtime, presence-check before use.

## Status per integration (1.16.5 → 1.20.1)

| Integration | 1.16 ref | 1.20.1 target | Disposition |
|---|---|---|---|
| **JEI** | 7.7.0.99 | **15.3.0.4** (in build) | Port categories — JEI v15 API differs substantially (`IRecipeCategory`, registration plugins). |
| **Curios** | 4.0.5.1 | 5.14.1 (compileOnly) | **Runtime disabled** in build — 5.14.1 mixin crashes on Forge 47.3.0 (`AccessorEntity f_19803_`). Guarded; keep compileOnly until upstream fix. |
| **ObserverLib** | 1.5.2 (HellFirePvP) | none published | **Inlined** as `common/structure/observer` package — port as first-party code, not a dependency. |
| **Patchouli** | 1.16.4-51 | has 1.20.1 | Decide: native Astral Tome vs Patchouli guidebook. Manifest node + Director call. |
| **Botania** | 1.16.5-416 | has 1.20.1 | Soft cross-mod integration — defer unless prioritized; guard. |
| **CraftTweaker** | 7.1.0.294 | has 1.20.1 | Recipe scripting hook — defer unless prioritized; guard. |
| **Corail Tombstone** | curse 3800673 | has 1.20.1 | Soft integration — defer unless prioritized; guard. |

## Rule

A `deferred` integration must (1) be `mandatory=false` in `mods.toml`, (2) be `compileOnly`
against its API, (3) have **all** call sites presence-guarded, and (4) carry an [[Escalation]]
record stating why it was deferred and what re-enabling it requires. That keeps the
[[Coverage Ledger]] honest — deferred, not dropped.
