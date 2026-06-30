# Week 4 — Shift Scheduling System

## Overview

You're building the backend for a shift scheduling system used by small businesses (think: cafes, retail stores, clinics) to manage employee shifts, time-off requests, and shift swaps. This is the kind of system real companies run their staffing on. It needs to behave correctly, not just look correct.

This spec describes only what the system does from the outside. How you build it — your layering, your patterns, your data structures — is entirely up to you.

No database is required this week. In-memory storage is fine, as it has been every week so far.

---

## Core concepts

**Employees** work at a business. Each employee has a name, an email, a role (e.g. "barista", "manager"), and a weekly availability pattern (which days/times they're generally able to work).

**Shifts** are scheduled blocks of time. A shift has a start time, an end time, a role requirement (e.g. this shift needs a "manager"), and is assigned to exactly one employee, or is unassigned.

**Time-off requests** are submitted by an employee for a date range. They can be approved or denied. An approved time-off request blocks that employee from being assigned to any shift that overlaps the requested range.

**Shift swap requests** let one employee propose trading their assigned shift with another employee's assigned shift, or just giving theirs away to be picked up. The receiving employee has to accept before the swap takes effect.

---

## Required behavior

### Employees

- Create, retrieve, update, and deactivate employees. Deactivating an employee is not the same as deleting them: their historical shift records must remain intact and queryable, but they can no longer be assigned to new shifts.
- An employee's weekly availability is expressed in a way that can answer: "is this employee generally available on Tuesday from 2pm to 6pm?"

### Shifts

- Create a shift with a start time, end time, and required role. Start time must be before end time. Shifts cannot be zero-length or negative-length.
- A shift can be assigned to an employee at creation time or later. Assigning a shift to an employee must be rejected if any of the following are true:
  - the employee is inactive
  - the employee's role doesn't match the shift's required role
  - the employee already has another shift that overlaps this one in time
  - the employee has an approved time-off request that overlaps this shift
  - the employee's stated weekly availability does not cover this shift's time window
- Unassigning a shift returns it to an unassigned state without deleting it.
- Shifts can be queried by date range, by employee, by role, and by assignment status (assigned vs unassigned), and these filters must be combinable in a single request.
- The system can report, for a given week, total scheduled hours per employee. This must correctly handle a shift that starts before the week begins or ends after the week ends, by only counting the portion of the shift that falls inside the requested week.

### Time-off requests

- An employee submits a time-off request for a start date and end date.
- A time-off request starts in a pending state. It must be explicitly approved or denied.
- Approving a time-off request that overlaps a shift the employee is _already assigned to_ must not silently succeed. The system needs to surface this conflict rather than approve the request and leave an inconsistent schedule behind. (You decide what "surface this conflict" means in terms of system behavior, but ignoring it is not acceptable.)
- Denied or pending time-off requests have no effect on shift assignment.
- An employee cannot submit a new time-off request that overlaps a date range they already have an approved time-off request for.

### Shift swaps

- An employee who is assigned to a shift can propose a swap, either targeting a specific other employee's specific shift (a direct trade) or leaving it open for any eligible employee to pick up (a giveaway).
- A direct trade swap is only valid if both employees would still satisfy every assignment rule above _after_ the trade (role match, no overlap, no time-off conflict, availability). Validate both sides, not just the proposer's side.
- A swap proposal can be accepted, declined, or withdrawn by the proposer before it's accepted.
- Once accepted, the shift assignments actually change. Once declined or withdrawn, nothing changes.
- A shift that is currently part of a pending swap proposal cannot be independently reassigned or deleted out from under the proposal. Decide what should happen to a pending proposal if its underlying shift becomes invalid some other way, and make that behavior consistent and intentional rather than accidental.

### Cross-cutting requirements

- All list-returning endpoints (shifts, employees, time-off requests, swap proposals) support pagination and return pagination metadata, not a bare array.
- Shift queries support filtering by date range, role, employee, and assignment status, combinable in a single request, as stated above.
- The system distinguishes, in its responses, between "the request was malformed" (missing fields, wrong types) and "the request was well-formed but violates a business rule" (e.g. double-booking, role mismatch, expired swap target). These should not be indistinguishable to a client.
- Every state-changing action (assign, unassign, approve, deny, propose swap, accept/decline/withdraw swap) should leave the system in a state where, if you queried everything related to that action immediately afterward, the results are fully consistent with what just happened. No stale or contradictory reads.

---

## What "done" looks like

A working API where:

- Every rule above is actually enforced, not just possible to satisfy if the client behaves well.
- The malformed-vs-business-rule-violation distinction is real and consistent across every endpoint, not handled differently in different places.
- Time and date handling is correct at the boundaries (shifts that span a week boundary, time-off ranges that touch but don't overlap, etc.) — these are exactly the kind of cases that look fine until you test them deliberately.
- You can describe, and defend, every design decision you made that this spec left open to you.

Good luck.
