# WPAI Constitution adoption

## Source and scope

Accepted `main` of
[MrWizard94-Compile/Agents-Constitution](https://github.com/MrWizard94-Compile/Agents-Constitution)
is the single editable source of constitutional law. Root and nested entries
load `wpai-constitution`; no local directory is an alternate law source.

This dated CI pin is accepted v6.16.3,
`89f8771df5a6fa8627cb9576afca1eefd0486d27`. New invocations resolve and freeze
accepted source using the skill; this pin is not permanently current law.
The ongoing consolidation invocation retains its earlier v6.16.2 freeze.

The migration adds a positive root entry, replaces two nested loaders, and
removes the Orchestrator's unconditional local-note precedence. Useful Obsidian
specification conventions from the pre-pack Claude guidance are retained in
the current nested CLAUDE note. Its obsolete backup is removed from the working
tree after exact recovery. The research transcript, validation ladder, other
architecture notes and all Obsidian configuration remain unchanged.

Historical recovery (not active law): `git show cbc93e63fda69bd30ee5fec3591e51d7b49984ac:Automation Architecture/CLAUDE.md.legacy-pre-pack-20260727-205752`

Review later edits before restoring history. The original entry pointers and
all other original tracked files are also recoverable at that base commit.

## Verification

The repository contains specifications, not an executable automation product.
Python 3.11 is a governance-development tool in CI, not a newly declared product
runtime. Both Windows and Linux jobs check the source pin and positive loader/
project-boundary/link contracts; a configured matrix is not a passing-run claim.

```powershell
python -X utf8 -W error -m unittest discover -s governance_tests -v
```

From a separately verified checkout of the exact accepted CI pin:

```powershell
python tools/validate-source.py
python -X utf8 -W error -m unittest discover -s tests -v
python tools/check-adoption.py C:\path\to\AutomationLab
```

Require each command to exit zero. The canonical audit and positive contracts
are complementary: absence of a retired name alone does not prove that a usable
loader exists. Actions use immutable commits, read-only repository permission
and non-persisted checkout credentials.

No model, external agent, service, memory seeding, port workload, Obsidian plugin,
publication or spending operation is run by these checks. This adoption does
not verify the historical transcript's provider/model claims, an implemented
runtime, every client's instruction reload, deployment or physical acceptance.
