The ordered, fail-closed gate sequence owned by [[AST_LSP]]: compile → Checkstyle → SpotBugs → datagen-validate → unit → GameTest → client-boot → [[Integration Gate]].

Each rung is real tooling, not opinion; the first failure emits a [[Flag]] and stops the ladder.
