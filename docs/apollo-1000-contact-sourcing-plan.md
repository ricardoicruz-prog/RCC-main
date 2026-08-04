# Sourcing Plan — 1,000-Contact Cycle

How to get from the current position (352 saved contacts, 103 already
contacted, ~39 immediately usable) to a 1,000-contact round.

Written 2026-08-04. Numbers marked ESTIMATE need confirming in the Apollo UI.

---

## 1. The list is not the binding constraint — sending capacity is

1,000 contacts × 4 emails = **4,000 sends**.

| Phase | Rate | Sends | Working days |
|---|---|---|---|
| Ramp (weeks 1-2) | 25/day × 4 inboxes = 100/day | 1,000 | 10 |
| Full rate | 40/day × 4 inboxes = 160/day | 3,000 | 19 |
| **Total sending window** | | **4,000** | **29 days ≈ 6 weeks** |

The last contact enrolled still has 20 days of sequence ahead of them, so
**the full cycle runs about 10 weeks end to end.** That is the real clock on
this plan. Building the list is a few days of work; running it is a quarter.

Two implications:

- Do not size the list beyond what the inboxes can send. 1,000 is close to the
  practical ceiling for one cycle on four inboxes. More contacts would need
  more inboxes, not more sourcing.
- Do not compress the ramp. The inboxes have four weeks of warming, not four
  months, and the last round already produced spam blocks.

## 2. Pool required

Approve rates observed on the existing never-contacted, still-on-list pool
(119 contacts, scored against the SOP tagging logic):

| Scenario | Approve rate | Raw contacts needed for 1,000 |
|---|---|---|
| Clean approvals only | 33% (39 of 119) | ~3,050 |
| Approvals + half of flagged clearing review | ~55% | ~1,800 |

Against available pool:

| Pool | Size |
|---|---|
| 7 states (pre-widening, confirmed) | ~1,100 |
| 12 states (widened) | ~1,800-1,900 **ESTIMATE** |
| Already saved | 352 (103 contacted) |

**The widened pool can just barely produce 1,000 — and only at the optimistic
55% rate, consuming essentially all of it.** That leaves nothing for the next
cycle and no margin if the estimate is high. The pool needs to be roughly
3,000 before a repeatable 1,000-contact cycle is comfortable.

## 3. How to expand the pool, in priority order

### 3.1 Add the 1-10 employee band — biggest lever, better ICP fit

Current bands are 11-20, 21-50, 51-100. The **1-10 band is excluded entirely**,
which is almost certainly the single largest source of missing volume: most
therapy and small clinical practices sit there.

It also fixes an existing mismatch. Owen is profiled at **5-30 employees**, so
the current floor of 11 cuts off the bottom half of the actual buyer, while
51-100 reaches past the top. Adding 1-10 aligns the search with the persona
rather than diluting it.

Caveat: the band also contains 1-3 person practices that are too small — no
team to reclaim hours for, no budget. Treat **fewer than ~5 employees as a
reject signal at scoring**, rather than excluding the whole band.

Consider dropping 51-100 at the same time if volume allows, since it overshoots
Owen. Do that only once the pool is comfortably above target.

### 3.2 Add practice types not currently covered

The current keyword list covers therapy, counseling, behavioral health, dental,
dermatology, eye care, urgent care, digestive, podiatry, physical therapy,
chiropractic, OB/GYN, gyms, fitness, yoga, med spa.

Candidate additions in the same ICP — owner-operated clinical practices with
the same admin burden:

orthodontics, oral surgery, periodontics, audiology, fertility/IVF, pain
management, sleep medicine, occupational therapy, speech therapy (standalone),
home health, veterinary, dietitian/nutrition practices, plastic surgery,
urology, allergy/immunology, primary care and family practice.

Veterinary is worth a deliberate decision — the operational story fits well,
but it is a genuinely different vertical and would need its own pain line.

### 3.3 Add states

Currently 12. Contiguous additions that stay regional: Kansas, Nebraska,
Arkansas, West Virginia, New York, New Jersey, Maryland, Virginia, North
Carolina, Georgia.

Cheapest lever mechanically, but it compounds the relevance-ranking problem —
see the state-by-state pulling rule in the SOP.

### 3.4 Loosen titles — last resort

Adding Practice Manager, Practice Administrator, or Managing Director would
expand the pool, but those are **Sam**, not Owen. Sam has visibility into the
pain and no budget. The current copy asks for a conversation about a decision
Sam cannot make. Only do this with copy written for Sam, and track it as a
separate lane.

## 4. Lane weighting

Do not split 1,000 evenly. Observed availability in the existing pool:

| Lane | Usable now |
|---|---|
| Mental Health | 21 |
| Medical Practice | 15 |
| Wellness/Fitness | 3 |

**Wellness/Fitness cannot supply a third of 1,000.** It has been the thinnest
lane at every measurement — 9 contacts enrolled in the entire program to date.
Weight the round toward Medical Practice and Mental Health, and either run
Wellness/Fitness as a deliberately smaller lane with no expectation of a
readable result, or park it for this cycle.

## 5. What 1,000 contacts is actually worth

Calibration, so the cycle is judged against something realistic:

| Reply rate | Replies | Positive (~35%) | Meetings (~40% of positive) |
|---|---|---|---|
| 1% (roughly what the old copy did) | 10 | 3-4 | 1-2 |
| 3% (decent cold email) | 30 | 10 | 4 |
| 5% (good copy, good targeting) | 50 | 17 | 7 |

**1,000 contacts is worth roughly 2-7 meetings per cycle.** Volume is doing
real work here — it takes the round from unmeasurable to measurable — but the
multiplier is reply rate, and that is a copy and targeting problem, not a
sourcing one. Ten times the contacts with the previous copy would have produced
about ten replies. The rewritten copy is what makes the volume worth buying.

## 6. Sequence of work

1. **[HUMAN ONLY]** Apply the filter changes in §3.1 and §3.2 to the saved
   searches in the People menu. Record the resulting pool size in
   `search-filter-spec.md` — this replaces the ~1,800 ESTIMATE with a real
   number and determines whether §3.3 is also needed.
2. **[HUMAN ONLY]** Pull contacts in batches of 50, "1 per company", never
   "Select all", **state by state**, saving to clearly named lists.
3. **[CLAUDE]** Merge the lists, dedupe against the 103 suppression set and the
   352 already saved, and score against the tagging logic.
4. **[EITHER]** Review flagged contacts. At ~45% flag rate, expect this to be
   the bulk of the review effort — budget for it.
5. **[EITHER]** Decide the fate of the 24 active and 3 paused contacts still
   mid-sequence on the old copy before enrolling anyone new.
6. **[CLAUDE / VA]** Enroll in the rewritten sequences, all four
   `meetricardo.co` inboxes in rotation, at the ramp in §1.

## 7. Open blockers

- The connector cannot write lists (label endpoints unauthorized), so list
  creation and merging happen in the UI until that scope is granted.
- The connector cannot read Apollo's prospecting database at all. Everything in
  §3 is a UI change; none of it can be automated from here.
- The three June Stage 2 sequences still point at `ricardo@ricardocruz.io` and
  must be repointed before reuse.
