# Rendering & GUI — 1.16.5 → 1.20.1

**Highest visual-parity risk in the whole port.** Astral Sorcery draws constellations, starlight
beams, halos, and overlays with custom buffers — the area least amenable to a pure deterministic
gate. Phase 3 escalates visual parity to the Director by design (see [[Escalation]]); the gate
proves it *compiles and boots without crashing*, the human confirms it *looks right*.

## Block entity & entity renderers

- `TileEntityRenderer` (TESR) → **`BlockEntityRenderer`**. Registration:
  `ClientRegistry.bindTileEntityRenderer(...)` → `BlockEntityRenderers.register(type, ctx -> new
  Renderer(ctx))`, or via `EntityRenderersEvent.RegisterRenderers` on the mod bus.
- `EntityRenderer` registration → `EntityRenderersEvent.RegisterRenderers` /
  `RegisterLayerDefinitions`.

## The matrix/buffer renames

| 1.16.5 | 1.20.1 |
|---|---|
| `MatrixStack` | `PoseStack` |
| `IRenderTypeBuffer` | `MultiBufferSource` |
| `IVertexBuilder` | `VertexConsumer` |
| `IBakedModel` | `BakedModel` |

## The real work: shader-based immediate draws

1.16 already used `RenderSystem`, but 1.17+ moved fixed-function calls to **core shaders**:

- `RenderSystem.color4f(...)` → `RenderSystem.setShaderColor(...)`.
- Binding a texture for a draw: `RenderSystem.setShaderTexture(0, rl)` + select a shader
  (`RenderSystem.setShader(GameRenderer::getPositionTexShader)` etc.).
- Immediate-mode draws: `Tesselator.getInstance().getBuilder()`, `builder.begin(VertexFormat.Mode,
  format)`, emit `.vertex(...).uv(...).color(...).normal(...).endVertex()`, then
  `BufferUploader.drawWithShader(builder.end())` (or `Tesselator#end`).
- Custom `RenderType`s: `RenderType.create(...)` with a `ShaderStateShard` — Astral Sorcery's beam
  / halo render types must select or define a shader. This is where most rewrite time goes.

> Verify the exact `RenderType`/shader builder calls against the MDK — these shifted again within
> the 1.17–1.20 window. The compile gate + a `runClient` smoke boot catch wiring errors; only a
> human catches "the beam renders but the blend mode is wrong."

## GUI (1.20's `GuiGraphics` cutover)

- `Screen#render(MatrixStack, ...)` → `Screen#render(GuiGraphics, int mouseX, int mouseY, float
  partialTick)`. **All draw calls moved onto `GuiGraphics`**: `guiGraphics.blit(...)`,
  `guiGraphics.drawString(...)`, `guiGraphics.fill(...)`, `guiGraphics.pose()`.
- Menus/screens: `Container`→`AbstractContainerMenu`, `ContainerScreen`→`AbstractContainerScreen`,
  `ContainerType`→`MenuType` (register via `DeferredRegister`).
- Particles: `IParticleData`→`ParticleOptions`; register `ParticleType` via `DeferredRegister`,
  factories via `RegisterParticleProvidersEvent`.

## Models

- Custom model loaders: `IModelGeometry`/`ISourceModel` → `IGeometryLoader` /
  `IUnbakedGeometry` (1.19+), registered via `ModelEvent.RegisterGeometryLoaders`.
- `ModelBakeEvent` → `ModelEvent.BakingCompleted`. `ItemOverrides`, `BakedModel` minor signature
  changes.
