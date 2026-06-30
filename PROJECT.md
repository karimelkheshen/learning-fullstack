# learning context and progress tracker

this document is the source of truth for an ongoing tutoring arrangement. at the end of every conversation, this file gets updated so the next session can pick up exactly where things left off. always read this before doing anything.

---

## who this person is

software developer and data engineer. works across both domains, writes scripts and application logic, models data, builds workflows. main tools are python, pandas, postgresql, mongodb, beautifulsoup, and selenium. already has solid general development experience.

**goal:** become significantly stronger at building full-stack applications. specifically: flask backend development, rest apis, and react frontend. wants this to help contribute more at current job, move into more software-focused work, or apply for other software engineering roles.

**learning style:** practice-first. prefers exercises, small projects, code reviews, and debugging tasks over theory. wants short recaps of prior concepts when returning. does not want explanations alone.

**availability:** 3-5 hours per week.

---

## skill assessment results (session 1)

assessed across python, software design, sql, mongodb, flask, pydantic, and react.

| area            | level                      | notes                                                                                                  |
| --------------- | -------------------------- | ------------------------------------------------------------------------------------------------------ |
| python core     | solid intuition, some gaps | missed mutable default argument trap, minor type details (args is tuple not list)                      |
| software design | above average              | correctly flagged layering, separation of concerns, defensive coding unprompted                        |
| sql             | rusty but logical          | subquery approach was correct, unaware of having clause                                                |
| mongodb         | practical understanding    | uses it at work, understands relational vs non-relational tradeoffs well                               |
| flask           | exposure only, not fluent  | used at current job but hasn't owned it end to end                                                     |
| pydantic        | good conceptually, one gap | confused pydantic models with orm/database models (pydantic = validation layer, sqlalchemy = db layer) |
| react           | zero                       | never used it, fresh start                                                                             |

**key pattern:** design thinking is genuinely strong, likely from data engineering background. gaps are at the implementation level. knows what should happen but hasn't written things enough times to own them.

**update after weeks 1-2:** this pattern held. every bug across both weeks was implementation-level (signature mismatches, enum value vs name, exception type mismatches), never a design-level mistake. layering, abstraction, and separation of concerns were correct from the first submission in both weeks.

**update after week 3:** pattern held again, with one new wrinkle. bugs were still implementation-level (a class used instead of an instance, a `sorted()` return value discarded), not design-level. but two of these bugs hid behind a fully green test suite, because the tests were written to confirm current behavior rather than to actually exercise the thing under test (e.g. a "sort" test built on input that was already sorted by construction). this person writes tests fluently now but needs to keep developing the instinct to construct adversarial/non-trivial test inputs, not just happy-path inputs that happen to pass. flagged directly, not yet a settled strength.

---

## framework decision

switched from fastapi to flask before week 1 started. flask is used at current job so there is immediate applicability. concepts transfer directly if fastapi is ever needed later and that would take about a week to pick up at that point.

---

## learning plan overview

three phases, 3-5 hours per week.

### phase 1 - backend foundations (weeks 1-4)

own flask properly. build a real api from scratch with correct layering, request validation, blueprints, and postgresql. no ai doing the heavy lifting.

**update:** phase 1 extended. originally weeks 1-4, then weeks 1-5 to allow a second flask-only week before introducing postgresql. then extended again: postgresql work pushed out further so the person could get more reps at flask api design and testing while still in-memory. week 4 is now the final no-database week, framed as a capstone for the in-memory/flask-only portion of phase 1, harder than week 3. postgresql + sqlalchemy + flask-migrate now begins week 5.

### phase 2 - react from zero (pushed back accordingly)

start fresh but move fast since api knowledge from the backend side already exists. focus: components, state, hooks, consuming rest apis.

### phase 3 - full-stack integration (pushed back accordingly)

connect everything. one small full-stack app end to end. react frontend talking to flask backend talking to a database.

---

## session log

### session 1

- ran full skill assessment across all target areas
- identified key gaps and strengths (see above)
- agreed on three-phase learning plan
- created this document
- **ended before starting week 1 exercise**

### between session 1 and session 2

- decided to switch from fastapi to flask (used at current job, immediate applicability)

### session 2 - week 1

- assigned book tracker api exercise (single resource, in-memory, pydantic validation, blueprints)
- three review rounds before clean, all implementation-level bugs (datetime/int mix-up, `**data` unpacking bypassing pydantic validation, `_books` dict at class level instead of instance level, missing id in PUT path, wrong status code on create)
- chose to keep blueprint-only error handlers for now (no app-level fallback), flagged as a known gap, not yet revisited
- week 1 closed clean

### session 3 - week 2

- person requested an extra week on flask before moving to postgresql
- assigned task manager api: two related resources (users, tasks), enums for status/priority, patch semantics, query param filtering, foreign-key-style validation (task owner must exist)
- review rounds caught 6 real bugs (missing status filter, unhandled crash on PATCH-not-found, recurring `**data` unpacking bug, broken partial-update logic, integer-valued enums leaking into json, manually-isoformatted datetime instead of native datetime)
- extended discussion on `TypeError` vs `ValidationError` as different failure modes, and enum name-lookup vs value-lookup being an api-contract decision, not something inherent to the enum
- dependency injection thread: walked from `flask.g` + `before_request` (wrong tool) through module globals, circular import risk, to the application factory + `ServicesContainer` dataclass pattern on `app.extensions`, which became the standing pattern
- week 2 closed clean

### session 4 - week 3

- agreed to delay postgresql further in favor of another in-memory rep, this time stepping up relationship complexity (many-to-many) and http correctness, not just resource count
- pytest introduced this week per direct request from session 3 notes. structured as two parts: (a) write tests against the already-working week 2 app first, to learn pytest mechanics against known-correct behavior, (b) write a new exercise with tests built alongside it
- **part a** (tests against week 2 app): first pass had a payload typo that accidentally caused a test to pass for the wrong reason (a missing required field, not the invalid enum value the test claimed to check). person caught and fixed it without much guidance. final suite covered fixture composition, parametrize, enum serialization regression coverage, and correctly chose 404 (not 400) for a nonexistent `owner_id` on task creation, a real api-design decision made deliberately rather than just matching existing behavior
- **part b** (new exercise, event rsvp system): events/attendees/rsvps, many-to-many relationship via rsvp as its own resource, capacity-driven waitlist promotion logic in the service layer, pagination with metadata, combined filter+sort+paginate on `GET /events`, 409 for conflict cases (closed/cancelled event, duplicate rsvp), 400 vs 422 distinction for malformed vs semantically-invalid input
- code review caught two real bugs that a fully green test suite did not surface:
  - `ServiceContainer` was referenced as the class itself, not instantiated (`service_container = ServiceContainer` with no `()`), causing every `create_app()` call to share the same singleton services across what should be independent app instances. invisible in a single-process test run, would surface in any deployment calling `create_app()` more than once
  - `sort_by_start_time_asc` was a no-op: `sorted(...)` was called but its return value was discarded, so results were never actually reordered. the corresponding test passed only because the test's fixture data happened to already be in sorted order by construction, so the test confirmed existing order rather than exercising sort logic against unsorted input
- both bugs fixed and confirmed by re-running the suite directly, not by code reading alone
- separately: 422 vs 400 distinction was an acknowledged oversight in the first pass (everything returned 400). resolved with a helper that checks whether all pydantic errors are `value_error` type (custom validator failures) vs structural (missing/malformed fields), with structural errors taking precedence in mixed-error cases. person reported the corresponding route and test updates as complete; this last round was not independently re-verified by me (person declined to re-paste code), unlike every other round this week which was actually re-run
- week 3 closed

---

## current position

**phase:** 1 - backend foundations
**week:** 4 (not yet started)
**active exercise:** none yet. week 4 is the final no-database, flask-only week, framed as a capstone before postgresql begins in week 5. by explicit request, the week 4 spec is being written as a user-facing description of the finished system only, no architecture hints, no implementation guidance, no suggested patterns. person wants to design the system cold this time. spec to be delivered as a standalone `.md` file per explicit request, not written inline in chat.

---

## architecture patterns established (carry forward, do not re-derive)

- layering: routes -> service -> repository, repository is an abc (or plain class, week 3 used plain classes without abc, both acceptable) with a concrete in-memory implementation per resource
- pydantic models are the single point of validation, never re-validate manually in function signatures with named params, always accept a `data: dict` and let `Model(**data)` raise `ValidationError`
- partial updates (PATCH) use `model_copy(update=data)` or equivalent dict-based merge, not named optional params with manual none-coalescing
- enums for constrained fields must be string-valued (`class X(str, Enum)`) so json serialization is human-readable, not integer-valued
- dependency wiring: application factory (`create_app()`) + a `ServicesContainer`/`ServiceContainer` dataclass stored on `app.extensions["services"]` or `app.extensions["services_container"]`, accessed in routes via `current_app.extensions[...]`. **must be instantiated with `()`, not referenced as the bare class** (real bug hit in week 3, costly because it's silent and only surfaces with multiple `create_app()` calls)
- rejected di patterns: `flask.g` + `before_request` (wrong tool, implies per-request scope for singletons), bare module-level globals (circular import risk), attaching services directly as attributes on `app` (fights flask's static typing)
- many-to-many relationships modeled as their own first-class resource (week 3: `Rsvp` linking `Attendee` and `Event`), not just a foreign key on one side
- status code discipline: 404 for "referenced resource does not exist" (e.g. nonexistent owner_id, attendee_id), 409 for state conflicts (duplicate rsvp, action against a closed/cancelled resource), 422 for semantically invalid input that is structurally well-formed (e.g. a date in the past), 400 reserved for structurally malformed input (missing/wrong-typed fields) and takes precedence over 422 when both error types are present in the same request
- pagination: return metadata (page, per_page, and similar) alongside results, not a bare list. query params for filters/sort/pagination should compose together on the same list endpoint
- known open gap: no app-level error handlers yet, only blueprint-level. flask will return html for errors outside registered blueprints (e.g. unmatched routes, 405s). not yet fixed, revisit when it actually causes a problem or during a dedicated cleanup pass. this would also be the natural home for centralizing the 400/422 decision instead of repeating it inline per route, if that pattern keeps showing up

---

## notes for next session claude

- do a one or two line recap of where things left off before starting
- keep the tone direct, do not over-explain things this person already knows
- when they submit code, review it critically and point out real issues, do not soften findings
- **run the code, don't just read it, especially for anything beyond trivial size.** week 3 had two real bugs that read as fine but were only caught by actually executing the app and tests. a green test suite is not sufficient evidence of correctness on its own, especially when the person is still developing the instinct to write adversarial test inputs rather than ones that happen to pass.
- this person asks "why" persistently when something doesn't fully click, especially around exception types and design pattern tradeoffs. answer the actual mechanism, not just "do it this way." they will push past a surface-level answer, so give the real one the first time.
- when stuck on a tooling/pattern question, they want to know what real production codebases do, not just "a way that works." give the production-realistic answer, then let them choose the level of complexity that fits their current project size, do not over-engineer preemptively, but be honest about what the simplification costs.
- when a fix is reported as done but not re-pasted/re-verified, note it honestly as unverified rather than implying the same confidence level as a re-run fix. don't dwell on it or make it a bigger deal than it is.
- requirements/exercise specs go in a standalone `.md` file when requested, not written inline in chat. check at the start of each new exercise whether this is still the preference.
- **week 4 is the final no-database flask week, explicitly framed as harder than week 3 and as a capstone.** the spec must be written purely from the end user's point of view, describing the finished system's behavior and capabilities only. no architecture hints, no implementation suggestions, no recommended patterns. this is intentional, the person wants to design the system cold this time without being steered.
- postgresql, sqlalchemy, and flask-migrate begin week 5, swapping in-memory repos for db-backed ones behind the same abstraction
- update this document at the end of every session
