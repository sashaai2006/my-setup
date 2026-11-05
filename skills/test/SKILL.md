---
name: test
description: Apply when designing, writing, reviewing, or refactoring automated tests.
type: prompt
whenToUse: When designing, writing, reviewing, or refactoring automated tests
disableModelInvocation: false
---

# Behavior-Focused Test Engineering

## 1. Understand Before Writing
- Inspect existing test framework, nearby tests, conventions, fixtures, helpers, and relevant production code.
- Identify the behavior to protect and the regression to detect.
- Do not modify production code when the request is test-only.

## 2. One Test, One Behavioral Intent
- Every test has one primary behavioral purpose; its name describes it.
- Do not bundle independent scenarios into one test.
- Multiple assertions are fine when they jointly establish one coherent outcome.

## 3. Test Names
- State expected behavior and the condition under which it occurs.
- Describe observable behavior, not implementation steps.
- Match the project's naming convention.

## 4. Test Structure
Use Arrange–Act–Assert:
1. **Arrange:** preconditions and input relevant to this test.
2. **Act:** the single operation under test.
3. **Assert:** focused assertion block.

## 5. Test Classification
Choose the narrowest appropriate test type and priority:

- **Type:** unit / integration / e2e / security / performance. Prefer unit tests for isolated logic; use heavier types only when the behavior crosses boundaries.
- **Priority:**
  - **P0** — blocker: core contract, security, data integrity, happy path that must never break.
  - **P1** — important feature path with workaround or critical edge case.
  - **P2** — normal edge case, error path, or secondary feature.
  - **P3/P4** — cosmetic, rare scenario, nice-to-have coverage.

Do not inflate priority to make tests look important. A test is P0 only if its failure blocks usage or introduces a critical risk.

## 6. Test Behavior, Not Implementation
- Prefer observable behavior and public contracts over private details.
- Derive expected results independently; never reproduce the production algorithm.
- Avoid tautological assertions.
- For bug fixes, add a regression test that fails before and passes after when practical.

## 7. Edge Cases and Independence
- Choose edge cases from the component's actual contract and failure modes.
- Tests are deterministic and independent: no shared state, randomness, wall-clock assumptions, or sleeps.
- Prefer a small set of high-value tests over many redundant ones.

## 8. When a Test Fails
- Classify the failure before fixing: test defect, product defect, environment issue, or unsupported assumption.
- For product defects, report severity and concrete repro steps. Do not silently adjust the test to make it pass.
- For P0/P1 failures, stop and report before continuing with unrelated work.

## 9. Completion Criteria
- Relevant test target ran and is green (or inability is reported).
- New/changed tests are discovered by the runner and exercise the intended path.
- Failures are classified and reported with severity and repro steps where applicable.
- Diff contains no unrelated changes.
- Report states behavior covered, checks run, priority distribution, and remaining gaps.
