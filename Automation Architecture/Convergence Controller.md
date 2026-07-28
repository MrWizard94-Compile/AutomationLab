Bounds the [[Executor]]⇄[[AST_LSP]] loop with max attempts and a global circuit breaker.

On exhaustion it routes [[Escalation]] to the [[User]] rather than looping forever. Fail-safe by construction.
