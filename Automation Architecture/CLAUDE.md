# Automation Architecture project conventions

Load [AGENTS.md](AGENTS.md) and the root entry first. Binding law comes from
the accepted [WPAI Constitution](https://github.com/MrWizard94-Compile/Agents-Constitution)
through `wpai-constitution`, not this project note. Freeze and verify one source
revision per invocation; the current invocation's freeze is not changed by an edit.

## What this is

This is an Obsidian specification vault, not a codebase. Each Markdown note is
one node in the design, and the wiki-link graph expresses relationships.
There is no declared product build, executable test or lint pipeline here.
The separate governance CI checks source identity and instruction routing only.

For an ambiguous request to implement or wire up a capability, establish whether
the target is these specifications or a separately authorized external codebase.
A documented component is not evidence that a running implementation exists.

## Architecture and editing conventions

The reviewed flow is [[User]] → [[Orchestrator]] → [[Executor]] → [[AST_LSP]],
with flags/revisions returning to the executor and accepted output returning to
the orchestrator through [[Integration Gate]]. [[REL]] and [[Smart Library]] are
specified orchestrator integrations; [[Asset Converter]] is an executor tool.
[[MCP]] describes transport, not proof of a deployed server.

Keep one terse, single-purpose concept per note. Link new concepts to their
neighbors and add the reciprocal links so the graph and backlinks remain useful.
Wiki links use the note base name, without `.md`; review each changed link in
the intended vault. Preserve the declared validation ladder and human approval
boundary. Do not imply that editing a note runs those gates.

Leave `.obsidian/` configuration to the application; do not hand-edit it for
content changes. The dated pre-migration conventions remain recoverable from
the source history named in the root adoption record; do not restore them as law.
