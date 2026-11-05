---
name: implement
description: Apply when implementing, changing, refactoring, or building code behavior.
type: prompt
whenToUse: When the user asks to implement, add, change, refactor, or build code behavior
disableModelInvocation: false
---

# Implementation Workflow

## 1. Understand Before Writing
- Read relevant code, callers, and contracts first. Reuse existing patterns.
- Define the target outcome and the check that will prove it.

## 2. Plan Only When Warranted
Write a short plan when the change spans files/modules, the approach is unclear, or it touches risky areas (concurrency, persistence, security, public API, migrations). Skip plans for trivial changes.

## 3. Scope Freeze
- Do exactly what was requested. Do not silently rename other symbols, extract helpers, add classes, change logic, or redesign architecture.
- If the task is "rename a function", change only the name and references. If broader cleanup seems necessary, ask first.

## 4. Implement Minimally
- Make the smallest complete change that satisfies the real requirement.
- Wire changes through all affected surfaces (callers, error paths, serialization, tests).
- No silent failures: propagate or surface errors explicitly.
- Preserve existing behavior; gate intentional behavior changes and cover with tests.
- Keep type safety; avoid casts that silence the compiler.

## 5. Completion Criteria
- Requested behavior is implemented and wired through affected surfaces.
- Defined checks actually ran and passed (or inability to run is reported).
- Required unchanged behavior is verified where checkable.
- Diff contains only in-scope changes.
- Handoff names files changed, checks run, and remaining limitations.
