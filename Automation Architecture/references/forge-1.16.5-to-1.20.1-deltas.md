# Master delta table — 1.16.5 (MCP) → 1.20.1 (official mappings)

Verify every exact signature against the live MDK; this is the conceptual map. Names below are
the **official/Mojmap** names used by the target build (`mappings channel: 'official'`).

## 1. Type renames (mechanical, but mappings-driven)

| 1.16.5 | 1.20.1 | Notes |
|---|---|---|
| `TileEntity` | `BlockEntity` | `TileEntityType` → `BlockEntityType` |
| `World` | `Level` | `ServerWorld`→`ServerLevel`, `ClientWorld`→`ClientLevel`, `IWorld`→`LevelAccessor`, `IWorldReader`→`LevelReader` |
| `PlayerEntity` | `Player` | `ServerPlayerEntity`→`ServerPlayer`, `ClientPlayerEntity`→`LocalPlayer` |
| `CompoundNBT` | `CompoundTag` | rename only — **NBT semantics identical, still used in 1.20.1** (`ListNBT`→`ListTag`, `INBT`→`Tag`) |
| `Vector3d` | `Vec3` | `Vector3i`→`Vec3i` |
| `ITextComponent` | `Component` | `new StringTextComponent(s)`→`Component.literal(s)`; `TranslationTextComponent`→`Component.translatable` |
| `ActionResultType` | `InteractionResult` | `ActionResult<T>`→`InteractionResultHolder<T>`, `Hand`→`InteractionHand` |
| `IParticleData` | `ParticleOptions` | particle registration via `DeferredRegister` |
| `Container` | `AbstractContainerMenu` | `ContainerType`→`MenuType`, `ContainerScreen`→`AbstractContainerScreen` |
| `IRecipe` / `IRecipeType` / `IRecipeSerializer` | `Recipe` / `RecipeType` / `RecipeSerializer` | serializer `read/write` → `fromJson/toNetwork`/`fromNetwork` |
| `Food` | `FoodProperties` | builder API |
| `ResourceLocation` | `ResourceLocation` | `new ResourceLocation(ns, path)` still valid in 1.20.1 (`fromNamespaceAndPath` is 1.21 — do **not** use) |

`IForgeRegistryEntry` base interface was **removed** (1.19). Registry objects no longer extend it.

## 2. Registration backbone

- Prefer **`DeferredRegister<T>` + `RegistryObject<T>`** (both present in Forge 1.20.1). Confirm
  whether the 1.16.5 source already uses `DeferredRegister` (likely) or `@ObjectHolder`/registry
  events (legacy) by scanning the [[Reference Source]].
- `RegistryEvent.Register<T>` (1.16) → consolidated **`RegisterEvent`** (1.18.2+); `DeferredRegister`
  hides this — register on the **mod event bus**.
- Vanilla registry references: `ForgeRegistries.BLOCKS/ITEMS/...` still exist; vanilla-keyed
  registries use `ResourceKey` via `Registries` / `BuiltInRegistries`.
- `@ObjectHolder` now **requires an explicit registry name** (1.19+) — migrate to `RegistryObject`.

## 3. Blocks & Items (two real traps)

- **`Material` was removed in 1.20.** `Block.Properties.create(Material.ROCK)` →
  `BlockBehaviour.Properties.of()` then compose explicitly:
  `.mapColor(MapColor.STONE).sound(SoundType.STONE).strength(...).requiresCorrectToolForDrops()`.
  Map each old `Material.*` to the right `MapColor` + `SoundType` + property flags.
- **Creative tabs changed (1.19.3).** `ItemGroup` → `CreativeModeTab`, and items **no longer set a
  tab in `Item.Properties`**. Either register a custom tab via
  `DeferredRegister<CreativeModeTab>` (`Registries.CREATIVE_MODE_TAB`) with a `displayItems`
  builder, or add entries via `BuildCreativeModeTabContentsEvent`.

## 4. Capabilities (stays Forge-style in 1.20.1)

- `@CapabilityInject` + `CapabilityManager.INSTANCE.register(...)` (1.16) →
  **`RegisterCapabilitiesEvent`** + `CapabilityManager.get(new CapabilityToken<T>(){})` (1.18+).
- `LazyOptional<T>`, `ICapabilityProvider`, `ICapabilitySerializable` **remain**. Persisted cap
  data still serializes to `CompoundTag`. (Do not migrate to attachments/data-components.)

## 5. Networking (near 1:1 in 1.20.1)

- `NetworkRegistry.newSimpleChannel(...)` + `channel.registerMessage(id, Msg.class, encode,
  decode, handle)` is **still the 1.20.1 Forge model**. Handler still takes
  `Supplier<NetworkEvent.Context>`; use `ctx.enqueueWork(...)`, `ctx.getSender()`, set
  `ctx.setPacketHandled(true)`. `PacketDistributor` unchanged.
- Do **not** rewrite to `CustomPacketPayload` / `StreamCodec` — that is 1.20.4+/NeoForge.

## 6. Recipes, tags, loot, data

- Recipes were already JSON in 1.16.5 — port custom **serializers** (signature changes) and
  generate vanilla-shaped recipes via datagen (`RecipeProvider`).
- **Tags: `ITag<T>` → `TagKey<T>` (1.18, big change).** References become `TagKey`s created with
  `BlockTags.create(rl)` / `ItemTags.create(rl)` / `TagKey.create(registry, rl)`.
- Loot: `LootContext` params and `LootTable` builders renamed; generate via `LootTableProvider`
  with sub-providers. The build's `data` run uses `--validate` — every emitted JSON is gated.

## 7. Lifecycle, events, mixins, AT

- Lifecycle events (`FMLCommonSetupEvent`, `FMLClientSetupEvent`, `InterModEnqueueEvent`, …) keep
  their names 1.16→1.20.1. `@Mod`, `@EventBusSubscriber`, mod-bus vs forge-bus split unchanged.
- **Mixins** target official-mapped names; refmap remapping is handled by the build
  (`mixin.env.remapRefMap=true`, `astralsorcery.refmap.json`). `@Shadow`/`@Accessor` use official
  member names — resolve against the MDK.
- **Access transformers** (`META-INF/accesstransformer.cfg`) use the same syntax but target
  official names now. The 1.16 reference shipped one; confirm whether the 1.20.1 build needs it
  re-declared (`minecraft { accessTransformer = file(...) }`) — this is a manifest entry.

## 8. Java 8 → 17

Additive for porting: records, sealed classes, `switch` expressions, `var`, text blocks all
available and encouraged for clean serializers/data holders. Watch for removed JDK internals
(`sun.misc.*`, Nashorn) — Astral Sorcery shouldn't touch these, but flag if the scan finds them.
