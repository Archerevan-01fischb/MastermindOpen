# Spec-Driven Project Pattern

Optional pattern for projects where the canonical artifact is a spec, not the code or content.

## When this fits

- **Game design** — design doc IS the source of truth; code follows the spec.
- **Documentation / content** — outline / spec drives generation; render is the side-effect.
- **API design** — OpenAPI spec is canonical; server + client are generated.
- **Reverse engineering** — RE notes are the spec; new implementation follows.

Common shape:

```
.specify/                    ← canonical specs
   ├── specs/
   │    ├── feature_a.md
   │    └── feature_b.md
   └── plans/
        └── feature_a_implementation.md  (derived from spec, hand-edited)

src/                        ← code that implements the spec
docs/                       ← rendered output (if a content project)
```

## GitHub Spec Kit

A common tooling choice is GitHub's open-source Spec Kit (search GitHub for the canonical repo — `github/spec-kit` or similar). It provides:

- A `.specify/` directory structure.
- A validator that checks spec ↔ implementation consistency.
- Optionally: a generator that emits boilerplate from the spec.

If you're new to spec-driven, Spec Kit is the easiest on-ramp.

## How mastermind helps spec-driven work

- **Drafts specs from conversation.** "Mastermind, write a spec for the new auth flow based on what we discussed yesterday." — mastermind drafts at `.specify/specs/auth.md`, includes invariants + acceptance criteria + open questions.
- **Compares spec ↔ implementation.** "Read `.specify/specs/auth.md` and the auth code, tell me what diverges." — mastermind walks both and reports drift.
- **Reverse-engineers existing code to specs.** "Read `src/auth/` and draft a spec capturing what's there." — mastermind creates a backwards spec, often a first step in a rewrite.

## Mastermind's "reverse-engineering directive" pattern

For RE projects specifically, mastermind has a known good pattern (the live mastermind has built this up; the public fork ships the core voice rules):

1. **Falsificationist discipline.** Assume your understanding of the existing system is wrong until proven by direct read of the source. Don't infer behavior from subagent summaries.
2. **Spec ↔ code parity check** at every revision. If the spec says X but the code does Y, one of them is wrong.
3. **Preserve user invariants** that aren't obvious from code (game-balance constants, UX timings, audio quirks).

See `memory/feedback_hallucination_pattern.md` and `memory/feedback_optimism_drift.md` for the voice rules behind this discipline.

## Project layout (suggested)

```
{project}/
├── CLAUDE.md                          (project-Claude or child instructions)
├── .specify/
│   ├── specs/                         (canonical sources)
│   │   ├── 001-feature-name.md
│   │   └── 002-another-feature.md
│   ├── plans/                         (implementation plans derived from specs)
│   └── reverse-engineering/           (if RE project — notes on the existing system)
├── src/                               (generated / hand-written implementation)
├── tests/                             (validation tests that pin spec invariants)
└── docs/                              (rendered output if a content project)
```

## Conventions

- **Specs are the source of truth.** When code and spec disagree, the spec usually wins (you change code to match) unless the spec is wrong (you change spec to match).
- **Open questions in specs are flagged.** Use a consistent marker (`TODO`, `OPEN QUESTION:`, `[?]`) so mastermind can grep for unresolved spec items.
- **Spec validators run in CI.** If a spec invariant is violated by code, the build fails.

## Read also

- `memory/feedback_first_principles_planning.md` — applies to spec drafting too: define what the thing DOES before listing files
- [child-mastermind-pattern.md](child-mastermind-pattern.md) — spec-driven projects often warrant a child Claude
- `templates/project-types/document-library/CLAUDE.md.template` — document-library type often uses spec-driven
