# BotForeman

**BotForeman** is an experimental agent orchestrator for the Copycat / SHRD research project.

Its job is not merely to call bots. The long-term idea is to **compose, stack and reuse bot capabilities** so that a group of small deterministic or specialized agents can behave like a larger tool without losing traceability.

> A bot has a skill.  
> BotForeman decides how skills work together.

## Core idea

A conventional orchestrator selects one tool for one task.

BotForeman is intended to go further:

```text
user intent
    ↓
BotForeman
    ↓
select bots
    ↓
stack capabilities
    ↓
execute
    ↓
evaluate
    ↓
KEEP / OMIT / UNCERTAIN
```

A useful sequence of capabilities can later become a reusable **macro-skill**.

For example:

```text
COUNT
  ↓
COMPARE
  ↓
TRACE
  ↓
STRUCTURAL_AUDIT
```

The resulting capability does not have to belong to any single bot.

## Why this exists

The project explores a simple question:

**Can small, inspectable agents be composed into more capable behavior while keeping the reasoning process testable, replayable and cost-aware?**

BotForeman is the layer responsible for that composition.

## Shatterglass

**Shatterglass** is currently treated as one possible structure for constraining an action, not as the whole orchestration system.

A Shatterglass can describe:

- what must remain invariant;
- what dimensions may change;
- what actions are allowed;
- how the result is checked.

A minimal abstraction is:

```text
SG = (r, D, A, C)
```

where:

- `r` = invariant;
- `D` = explorable dimensions;
- `A` = allowed actions;
- `C` = validation criteria.

BotForeman may then compose capabilities under those constraints.

## Current direction

The planned architecture includes:

- a bot registry;
- capability / skill metadata;
- deterministic evaluators;
- capability stacking;
- reusable macro-skills;
- execution traces;
- cost and token accounting;
- replayable runs;
- optional Shatterglass constraints;
- a chat-driven control layer;
- Codex-assisted implementation and testing.

## UI concept

BotForeman is intended to grow into a small simulator / cockpit rather than remain only a command-line orchestrator.

A possible layout:

```text
┌──────────────┬──────────────────────┬─────────────────┐
│ Chat         │ Agent / Skill Graph  │ Execution Trace │
│              │                      │                 │
│ instructions │ active stack         │ decisions       │
│ constraints  │ dependencies         │ evaluations     │
└──────────────┴──────────────────────┴─────────────────┘
│ cost • tokens • run history • replay                  │
└────────────────────────────────────────────────────────┘
```

The chat is the semantic command surface. BotForeman translates intent into agent composition; Codex can act as the implementation worker underneath that control layer.

## Design principles

1. **Composition over monoliths**  
   Prefer small capabilities that can be recombined.

2. **Determinism where possible**  
   A deterministic checker should stay deterministic.

3. **Traceability**  
   Every composed action should be inspectable.

4. **No silent rewriting**  
   Evaluators judge results; they should not quietly replace them.

5. **Cost awareness**  
   More agents are not automatically better. A stack must justify its cost.

6. **Reusable discoveries**  
   Successful stacks should be promotable into named macro-skills.

7. **Constraints remain explicit**  
   Invariants and evaluation criteria should be visible rather than hidden inside prompts.

## Relationship to Copycat

Copycat is the language-learning experiment.

BotForeman is the orchestration layer that can eventually coordinate evaluators, teachers, deterministic bots, diagnostic tools and coding agents around that experiment.

The two projects can evolve independently.

## Status

**Experimental / prototype.**

The architecture is intentionally small enough to change as the experiments reveal which abstractions are actually useful.

---

Part of the broader **Copycat / SHRD** experimental workspace.
