# JOURNAL

My running record of progress through Module 3 on the pathreview project. One section per week.

## Week 7: Issue Selection

**Issue link:** https://github.com/jamjamgobambam/pathreview/issues/50

**Issue title:** Add a `has_tests` boolean to the repo analysis output

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
PathReview's agent layer has a GitHub tool (`agent/tools/github_tool.py`) that pulls repository metadata such as the name, primary language, star and fork counts, and whether a README exists, then returns it as a structured dict the reviewer reads when it assesses a candidate's projects. Right now that output includes a `has_readme` flag but carries no signal for whether a repository actually ships automated tests, even though "does this project have tests?" is a real indicator of portfolio quality. Because the field is missing, that information never reaches the reviewer, so a project's testing story cannot be rewarded or flagged. A successful fix adds a `has_tests` boolean to the output, worked out the same way `has_readme` already is, by checking the repository contents for common test locations such as `tests/`, `test/`, `__tests__/`, `spec/`, and `pytest.ini`. It would add a small `_has_tests` helper that mirrors the existing `_has_readme` helper, place `"has_tests"` next to `"has_readme"` in the metadata dict, and cover it with unit tests for repositories that do and do not contain tests. The work stays inside the agent tools subsystem and only adds to the output.

**Branch name:** `feat/50-repo-analysis-has-tests`

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger

### Is this issue right for me? Scope reasoning

This is my first time contributing to a codebase this large, so a Tier 1 "good first issue" matches where I am right now, and I picked it on purpose rather than because it looked interesting. Here is how I reasoned about the fit:

* The scope is small and stays in one place: one new field on one tool's output, with no schema migrations and no wide refactor.
* The effort is roughly 2 to 4 hours, which lines up with the issue's own Tier 1 estimate.
* The skills it needs are ones I have or can pick up quickly: Python, `httpx` for the GitHub REST call, `pytest` with `unittest.mock` for the tests, and a basic grasp of the GitHub contents API.
* The files it touches are few: `agent/tools/github_tool.py` for the helper and the new metadata key, plus a new `tests/unit/test_github_tool.py`, and `api/schemas/review.py` only if the field ends up exposed through the API.
* There is a clear precedent and no blockers: the existing `_has_readme` helper is an exact pattern to copy, so the path is obvious.
* I checked that it is genuinely doable before claiming it: `has_tests` really is absent from `agent/tools/github_tool.py`. The similarly named `ingestion/parsers/repo_analyzer.py` already has a `has_tests` field, so the agent GitHub tool is the one that still needs it, and that is my target.

### Setup notes

* Backing services start in the background with `docker compose up` (Postgres on 5433, Redis on 6379). ChromaDB's 0.4.22 image currently crashes on start because of an upstream NumPy 2.0 change (`np.float_` was removed), but it is not needed to run the frontend, and `make setup` and `make run` both finish without it.
* `make setup` applied migrations 001 and 002, seeded the test accounts (user1@example.com through user3@example.com), and installed the frontend dependencies.
* `make run` serves the frontend at http://localhost:5173 and the API at http://localhost:8000/docs, and I confirmed both return HTTP 200.
