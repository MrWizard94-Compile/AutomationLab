The QA gate: runs the deterministic [[Verification Ladder]] (compile, lint, schema, unit, GameTest, integration) **fail-closed** — it approves nothing on opinion.

Emits structured [[Flag]]s to the [[Executor]] for revision and passes only all-green output up to the [[Orchestrator]].
