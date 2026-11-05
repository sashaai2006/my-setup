---
name: git
description: Conventional Commits workflow for writing, reviewing, and rewording commit messages.
type: prompt
whenToUse: When the user asks to commit, write or reword a commit message, review commit history, or prepare changes for commit.
disableModelInvocation: false
---

Commit message and commit workflow rules based on Conventional Commits 1.0.0. Use whenever the user asks to commit, write or reword a commit message, review commit history, or prepare changes for commit, even if they do not mention "conventional commits".

Git: Conventional Commits

Scope of this skill: commits, commit messages, and pull-request summary workflow. Branching, rebasing, and pushing are not covered here.

1. Resolve the format first

Follow the first source that exists:

The project's own rules (CONTRIBUTING, commitlint config, project AGENTS.md).
The established convention in git log --oneline -20, if consistent.
Otherwise, Conventional Commits as described below.

Never impose feat:/fix: on a repository that uses a different established format.

2. Message format
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
type: feat (new feature, SemVer MINOR) and fix (bug fix, SemVer PATCH) are the only types the spec requires. Common additional types: docs, style, refactor, perf, test, build, ci, chore, revert.
scope: a noun in parentheses naming the affected area, e.g. feat(parser):. Optional; omit it if no single area fits.
description: directly after : . Short, imperative mood, no trailing period, about 72 characters max (convention, not spec).
body: starts after one blank line. Explain what and why, not how.
footers: start after one blank line following the body. Format is Token: value or Token #value. Tokens use - instead of spaces (e.g. Reviewed-by, Refs), except BREAKING CHANGE.
breaking change (SemVer MAJOR): add ! right before the colon, and/or a footer BREAKING CHANGE: <what breaks and how to migrate> (uppercase). If ! is used, the footer may be omitted, but then the description must state the break.

Type keywords are always English. The description language follows existing history; default is English.

3. Choosing the type
Type    Use when
feat    New user-visible capability
fix    Bug fix
refactor    Code change that neither fixes a bug nor adds a feature
perf    Change that improves performance
test    Adding or correcting tests only
docs    Documentation only
style    Formatting only, no behavior change
build    Build system or dependency changes
ci    CI configuration
chore    Maintenance that fits none of the above
revert    Reverting an earlier commit (reference its hash in a Refs: footer)

Pick the type from the actual diff, not from the user's wording alone. One commit is one logical change; if the diff mixes types, propose splitting it.

4. Workflow
Inspect read-only: git status, git diff (staged and unstaged), and git log for the convention.
Draft the message and list exactly which files or hunks it covers.
Show the draft and wait for explicit approval. git add, git commit, and every other state-changing command require it.
After committing, report the resulting hash and subject.
Do not push yet. Proceed to section 5 to prepare the PR summary first.

Do not:

skip hooks (--no-verify) unless the user explicitly asks; if a hook fails, fix the cause or report it;
amend, squash, or rewrite existing commits unless the user explicitly asks.
5. Pull Request summary workflow

Before pushing the branch or creating a PR, inspect the diff of the branch against the base branch (`git diff <base>...<branch>`). Produce a concise markdown summary for the user in the chat. The summary must include:

- **What was done:** a detailed but concise explanation of the changes introduced by this branch. Describe the intent, the behavior, and any important implementation choices. Do not list individual files.
- **Impact:** what changes as a result of this branch. Include measurable results or comparisons where possible (e.g., metrics, benchmarks, test outcomes). For changes where measurement is not applicable, describe the expected behavioral or experiential effect (e.g., "player now hears echoes from every wall", "creature reacts faster").
- **Risks / things to watch out for (optional):** potential side effects, breaking changes, incomplete parts, or areas that need extra attention. Omit this section if there are no meaningful risks.

Do not include:
- A list of changed files.
- A checklist of tests or commands run.

Show the summary and wait for explicit user approval before pushing the branch.

After approval:
1. Push the branch.
2. Create a PR using the approved summary as the PR description.
3. Show the PR link and wait for explicit user approval before proceeding with `git merge`, `gh pr merge`, or any other state-changing command that lands the branch.
6. Examples
feat(auth): add refresh token rotation
fix: prevent crash on empty config file
fix(api): return 404 for unknown user ids

The handler fell through to a 500 when the lookup returned nothing.

Refs: #214
refactor(parser)!: drop legacy include syntax

BREAKING CHANGE: `@include` is no longer parsed; use `import` instead.
