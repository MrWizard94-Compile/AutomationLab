Reconciles 100% of [[Port Manifest]] entries at delivery: each is either `passed` or `deferred` with a justification and an [[Escalation]] record.

Enforces no silent drops. Owned by the [[Orchestrator]]; delivery is refused while any entry is still `pending` or `in_progress`.
