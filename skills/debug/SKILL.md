---
name: debug
description: Apply when debugging, diagnosing, or fixing a bug, crash, test failure, or incorrect behavior.
type: prompt
whenToUse: When debugging, diagnosing, or fixing a bug, crash, test failure, or incorrect behavior
disableModelInvocation: false
---

# Evidence-Driven Debugging

## 1. Reproduce Before Fixing
- Reproduce with the actual failing test/command/script. A bug not reproduced is a hypothesis.
- If reproduction is impossible, say so and state the evidence you have.
- Capture the exact failure signature; fixes must address it.

## 2. One Hypothesis at a Time
- Form one falsifiable hypothesis; design the cheapest experiment to test it.
- Change one thing at a time. Revert refuted edits before the next hypothesis.
- If two consecutive hypotheses fail, stop and reassess from evidence.

## 3. Fix the Root Cause
- The fix must explain why the failure occurred.
- Do not weaken checks, delete assertions, add broad catches, or special-case the failing input.
- Fix at the correct layer.

## 4. Prove the Fix
- Add a regression test that fails before and passes after, when practical.
- Re-run the original reproduction; the failure signature must be gone.
- Run surrounding tests for collateral damage.
