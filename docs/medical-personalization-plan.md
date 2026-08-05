# Medical Sequence — Personalization Path Forward

Response to Apollo's automated sequence review of *RCC Time Recovery — Medical
Practice (v3, A/B)*, and a staged plan for adding real personalization.

Written 2026-08-05.

---

## 1. First: the metrics in that review are not yet real

Apollo's review reports **923 contacts, 0 replies, 0% reply rate**. Pulled
directly from the sequence, the actual state is:

| Metric | Value |
|---|---|
| Contacts scheduled | 920 |
| **Emails actually delivered** | **109** |
| Hard bounces | 2 (1.8% of attempted) |
| Unique opens (unfiltered) | 32 of 109 — 29% |
| Replies | 0 |
| First send | today |

**811 of the 920 have not received a single email yet**, and the 109 who have
got theirs today. Cold email replies arrive over roughly 2–14 days; almost
nobody replies within hours. At a healthy 3% reply rate, 109 delivered emails
would be expected to yield around three replies — spread across the next two
weeks, not this afternoon.

So "0% reply rate" here is not a finding. It is the absence of data, and it is
the same trap as the original 101-contact round: reading a number before it can
possibly mean anything. **Do not change the copy because of that number.**

What the early numbers *do* say, tentatively: a 1.8% hard bounce rate is
acceptable (watch it, act above 5%), and a 29% unfiltered open on day one is
unremarkable in either direction.

**The right read date is 2026-08-19** — roughly two weeks out, once most of the
920 have received at least touch 1 and touch 2.

## 2. Which recommendations are worth acting on

| Apollo's recommendation | Verdict |
|---|---|
| "Lacking meaningful personalization beyond basic fields" | **Valid.** The copy uses only `{{first_name}}` and `{{company}}`. This is the real gap and section 3 addresses it. |
| "Weak opening hook — generic opener" | **Partly valid.** The opener is a deliberate category observation rather than fake intimacy, which is right, but it is not specific to the recipient's business. Fixable cheaply. |
| "Follow-up emails repeat the same messaging" | **Not accurate.** The four touches are distinct: a pain question, the hiring-doesn't-fix-it story, the cost arithmetic, and a breakup. This reads like a template criticism that did not parse the actual content. No action. |
| "Vary subject lines and lead angles per step" | **Already done across steps** — intake process / the hire that didn't fix it / the math on 15 hours / closing the loop. |
| "…per step to reduce repetition across A/B variants" | **Do not do this.** Variants A and B deliberately share subject lines. That is what makes the ask — reply vs click — the single variable under test. Varying subjects between A and B would confound the experiment and waste the round. |

## 3. Tiered personalization plan

Do not attempt to hand-write 923 emails. Tier the effort so most of the lift
comes at near-zero cost, and reserve deep research for where it pays.

### Tier A — specialty-specific pain line (free, covers all 923)

The single biggest cheap win. Right now every medical contact receives the same
line:

> patient intake, billing, and supply coordination

That is sent identically to a dental practice, an eye clinic, a physical
therapy clinic and a podiatrist. The NAICS code already held on every contact
splits them, and each specialty has a different daily grind:

| NAICS | Specialty | Pain line |
|---|---|---|
| 6211 | Physicians | patient intake, prior authorizations, and referral coordination |
| 6212 | Dental | insurance pre-authorisations, treatment plan follow-ups, and recall scheduling |
| 62131 | Chiropractic | new patient intake, insurance billing, and re-exam scheduling |
| 62132 | Optometry | insurance verification, frame and lens ordering, and recall reminders |
| 62134 | PT / OT / speech | visit authorisations, progress notes, and re-certification paperwork |
| 62139 | Other practitioners | patient intake, billing, and supply coordination *(current default)* |

No research, no credits, no new data. It turns a generic line into one that
reads as though it was written for that kind of practice — which for a cold
opener is most of the benefit of personalization, without the fragility of
fake specificity.

### Tier B — hiring trigger (1 credit per company)

The strongest available trigger, and it is *already* the argument of email 2.
`apollo_organizations_job_postings` returns current openings. A practice
actively advertising for a front desk coordinator, patient coordinator, billing
specialist or office manager is, right now, doing the exact thing email 2 says
does not work.

That yields an opener that is specific, true, and impossible to fake:

> Saw you're hiring a patient coordinator at {{company}}. Worth saying — most
> practices I work with found that role got swallowed by the same manual
> intake and billing work within a quarter.

**Cost: exactly 1 credit per company.** With 1,417 credits left this cycle
(resetting the 20th), checking all 923 is not affordable alongside anything
else. Suggested scope: **200–300 companies**, chosen from the best-fit end of
the list. Roughly 15–25% typically have a relevant opening; those become a
distinct high-signal segment.

### Tier C — hand-researched openers (50–100 contacts)

For the highest-value accounts only: real research (site, recent news,
leadership pages) and a hand-written first line. Expensive per contact, so
reserve it for accounts worth a bespoke effort.

### Delivery mechanism

Apollo supports per-contact bodies through contact custom fields used as merge
variables: store the personalized line on the contact, reference the field by
name in the template, and Apollo resolves it per recipient at send.

Three practical notes:

- Five contact custom fields already exist, left over from earlier Apollo AI
  enrichment runs — including two "Persona Intelligence" textareas, one of
  which already holds a generated summary on at least some contacts. They are
  usable, but their auto-generated labels ("Persona Intelligence 9348
  0621233354") make poor merge variables.
- **Creating a cleanly named field looks like a UI-only step** — no
  field-creation tool resolved on this connector, only `apollo_fields_index`.
  Create `custom_opener_medical` in the UI; populating it per contact is then
  scriptable via `apollo_contacts_update`.
- Always set a sensible fallback. If the variable is empty for a contact, the
  sentence must still read correctly — this is where personalization most
  often breaks in production.

## 4. The timing problem — needs a decision

811 contacts have not yet received touch 1. Changing email 1 now means part of
the audience gets the generic version and part gets a personalized one, mixed
across both A/B arms. That does not just muddy the personalization result; it
**breaks the reply-vs-click test currently running**, which is the thing this
round was built to answer.

Three options:

1. **Let the round finish, personalize the next one.** Cleanest data. The A/B
   answers reply-vs-click, and personalization becomes the next single
   variable. Slowest, but every result stays attributable.
2. **Pause Medical now, personalize, relaunch.** Fastest to a personalized
   send, but discards the 109 already delivered and abandons the A/B before it
   can produce anything.
3. **Treat the remaining 811 as a deliberate third arm** — generic vs
   personalized, tracked separately. Salvages the volume but means two
   variables moving at once, so a difference cannot be cleanly attributed.

**Recommendation: option 1**, with Tier A prepared and staged now so it is
ready to deploy the moment this round reads out on 19 August. Tier A costs
nothing to prepare and can be written while the current round runs.

The exception worth considering: if the 19 August read shows a genuinely dead
reply rate across both arms, that is the signal to stop the round early and
move to personalization rather than let the remaining touches burn.

## 5. Sequence of work

1. **Now:** draft the six specialty pain lines (Tier A) and map each of the 923
   contacts to a specialty from its NAICS code. No credits, no Apollo changes.
2. **Now:** create the `custom_opener_medical` contact field in the Apollo UI.
3. **2026-08-19:** read the round — reply rate overall, and A vs B. This is the
   first date the numbers mean anything.
4. **Then:** deploy Tier A to the next round as the single changed variable.
5. **Optional, if credits allow after the 20th reset:** Tier B hiring triggers
   on a 200–300 company subset.
