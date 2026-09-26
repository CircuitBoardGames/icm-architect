# Hub adaptation — CircuitBoardGames/ClaudeCode and its box

This file exists only in the CircuitBoardGames fork. Where it disagrees with `SKILL.md` or the other
references, **this file wins on the hub**. Upstream's method is unchanged. This file says where the
hub already carries it, so a session does not build a second copy.

## The hub is already an ICM. Do not restructure its instruction surfaces

The hub's layers are delivered by the harness, not by convention, and that is stronger than a
`CONTEXT.md` an agent has to choose to open:

| ICM layer | On the hub |
|---|---|
| L0 entry file | `AGENTS.md`. Its size is governed by `.claude/rules/claude-md-budget.md`, not by the ~60-line target |
| L1/L2 contracts | `.claude/rules/*.md` with `paths:` frontmatter, injected when a matching tree is touched |
| L3 reference | `docs/agents/` (runbooks), the Wiki-Vault repo (`wiki/gotchas/`) |
| L4 product | per-task worktrees and their PRs |

So, in the hub repo:

- **No `CONTEXT.md` per folder.** A folder that needs a contract gets a path-scoped rule.
- **No `AGENTS.md` / `routing.md` twins.** Claude Code and omp both load `AGENTS.md`, and a
  twin is one more always-loaded surface to keep in sync.
- **Never propose shrinking `AGENTS.md` to the ICM target.** Moving content out of it follows
  `claude-md-budget.md`; `.claude/hooks/instruction-file-guard.py` delivers that rule on edit.
- **The Wiki-Vault is out of scope.** Its conventions are claude-obsidian's plus OKF's `type`
  frontmatter; the Knowledge-bundle form would compete with them.

## What it is for here

1. **Restructure mode on a carve-out** (files leaving one hub repo for another). This is the main
   use. Run step 4 (`reference-integrity.md`) as written. On this box the external referrers it asks
   about are enumerable, so search them rather than only asking the owner:
   - `/etc/cron.d/`, `/etc/systemd/system/`, symlinks in `/usr/local/bin/`;
   - every sibling checkout under `/home/claudeadmin/` (Box-Ops, AgentOS, Wiki-Vault, …), plus
     `/opt/agentos-src` and `/var/lib/agentos/`;
   - `.claude/settings.json` hooks and `~/.claude/settings.json`;
   - forge issues and PR bodies that cite the path (the listing caps at 50, so page it).

   Search with `git grep` or `command grep -rn`. **A bare `grep` in a Bash call is ugrep and silently
   skips gitignored files**, so it reports "no referrers" for files it never read. Before trusting an
   empty search, show it finds a path you know is referenced.
2. **System map form on a target repo** an agent will edit. Put `map/` at the target's root: it is
   content, which the hub's target-repo rule allows (CI and graphs, never vendored tooling). The
   understand-anything graph is the generated half, so link to it rather than re-deriving structure.
   `status: verified` carries a commit sha.

## How the hub's workflow maps onto the method's gates

- The **human approval gate** (Restructure step 5) is the PR review. For a carve-out that crosses
  repos, the operator approves the migration map before any PR is opened.
- **Copy, verify, remove** happens in a worktree made by `scripts/worktree-create.sh`, never in the
  reference checkout. The parity check is the forge's CI on the PR, plus the referrer search above
  re-run against the result.
- Case-folded destination collisions cannot happen on this ext4 box. They still matter for a
  checkout on a macOS laptop, so keep the check when a move renames by case only.
