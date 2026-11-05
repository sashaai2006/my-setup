---
name: audit
description: Apply when reviewing, auditing, inspecting, or finding defects in code.
type: prompt
whenToUse: When reviewing, auditing, inspecting, or finding defects in code
disableModelInvocation: false
---

# Evidence-Based Code Audit

## Scope
- Treat audit/review as read-only unless the user explicitly asks for fixes.
- Establish scope, architecture, build/test entry points, trust boundaries, and call paths before concluding.
- Coverage is defined by boundaries. If anything in scope is uninspected, list it explicitly.

## Areas to Assess (proportional to risk)
- Correctness: invariants, state machines, error paths, boundaries.
- Memory/resource safety: leaks, use-after-free, cleanup, exhaustion.
- Concurrency: races, deadlocks, ordering, lifetime races.
- Security: input validation, trust boundaries, injection, secrets, TOCTOU.
- Reliability: retries, timeouts, idempotency, shutdown.
- Verification: test gaps, ineffective assertions, missing negative/boundary cases.

## Standard for a Finding
Every finding needs:
1. Severity and confidence.
2. Precise file/line reference.
3. Violated contract/invariant.
4. Triggering conditions or minimal scenario.
5. Likely impact.
6. Validation or remediation direction.

Do not report style as bugs. Do not promote theoretical possibilities to confirmed defects. Rank by real risk.

## Completion Criteria
- All in-scope boundaries, entry points, and error paths are inspected or listed as uninspected.
- Every finding satisfies the six-field standard.
- Report leads with highest-risk findings, then rejected hypotheses, checks run, and unresolved areas.
- Never claim a clean bill of health from a quick scan.
