# Apollo Sequence Copy Review — August 2026

Review of the five sent RCC sequences, plus rewritten copy for the next
campaign. Nothing here has been deployed to Apollo.

Sources: Apollo analytics (all-time, pulled 2026-08-04), deployed copy from
`rcc-cold-outreach-sop/references/email-templates.md`, buyer profile from
`rcc-personas` (Owen — Overwhelmed Owner). Rewrite applies the
`email-sequence` and `email-marketing` skills.

---

## 1. What the data actually says

| Sequence | Contacts | Sent | Delivered | Unique opens | Open rate | Replies |
|---|---|---|---|---|---|---|
| Medical Practice (Stage 2) | 40 | 161 | 160 | 9 | 22.5% | 0 |
| Mental Health (Stage 2) | 27 | 103 | 103 | 11 | 40.7% | 0 |
| Wellness Fitness (Stage 2) | 9 | 37 | 36 | 2 | 22.2% | 0 |
| MH Owners V2 — Variant A (Founder Dependency) | 13 | 39 | 39 | 1 | 7.7% | 0 |
| MH Owners V2 — Variant B (Admin Capacity) | 12 | 34 | 34 | 3 | 25.0% | 1 |
| **Total** | **101** | **374** | **372** | **26** | — | **1** |

### The sample is too small to diagnose copy

101 contacts across five sequences. Largest single sequence: 40 contacts.

This is the most important finding in the review. At 101 contacts, a campaign
whose copy is performing at a perfectly healthy 3% reply rate would still
produce 1 or fewer replies roughly 19% of the time. One reply in 101 is not
evidence that the copy failed. It is a sample too small to distinguish good
copy from bad copy at all.

Detecting the difference between a 1% and a 4% reply rate with any confidence
takes roughly 300–500 contacts *per variant*. The A/B test between Variant A
and Variant B — 13 contacts versus 12 — cannot support any conclusion. Variant
B "winning" 1–0 is a coin flip.

The copy does have real, fixable problems (section 2). But they were found by
reading it against cold-email fundamentals, not by inferring them from the
reply count. The reply count cannot carry that weight.

### Deliverability was not entirely clean

The brief assumed deliverability was fine. Mostly it was, but three signals say
otherwise:

- **Spam blocks.** Wellness Fitness had a 10% spam-block rate (1 of 9
  contacts). Medical Practice had 2.4% (1 of 40).
- **Unsubscribe.** Mental Health (Stage 2) had a 3.7% opt-out rate — 1 of 27
  contacts. For cold outbound at this volume that is high.
- **Variant A's 7.7% open rate** sits far below the 22–41% of every other
  sequence. A gap that size is more typically inbox placement than subject-line
  quality.

Treat open rates here as directional only. Apollo reports `open_rate_unfiltered`
of 100% on three sequences, which means bot and scanner opens are being
filtered out — the underlying tracking is noisy.

None of this is a crisis. But "deliverability was fine, so it must be the copy"
is not supported, and the link-in-every-email pattern (section 2) is a
plausible contributor to the spam blocks.

### Volume, not copy, is the binding constraint

101 contacts over roughly six weeks. Rewriting copy and relaunching at this
volume will produce another unreadable result. The rewrite below is worth
shipping, but it needs meaningfully more volume behind it — on the order of
300+ contacts per lane — before its performance means anything.

---

## 2. What is wrong with the current copy

Read against the deployed templates. Ordered by expected impact.

### 2.1 The emails never ask for a reply

This is the single biggest issue and the most likely cause of zero replies.

All four emails end by pointing at `ricardocruz.io/hello`. Not one of them asks
a question. The only action offered is a click. The sequence is optimized to
generate clicks, and it is being measured on replies — two different things,
and it is getting neither (4 clicks total across 374 sends).

Cold email replies come from asking one easy, specific question. A URL is not a
question.

### 2.2 The emails are three to four times too long

Apollo's own guidance: 25–85 words, with ≤50 words correlating to materially
higher reply rates. Current lengths:

- Email 1: ~200 words
- Email 2: ~230 words
- Email 3: ~200 words
- Email 4: ~130 words

Email 2 is a five-paragraph essay sent to a stranger who did not ask for it.

### 2.3 A tracked link in email 1, and in every email after

A first-touch cold email from an unknown sender containing a tracked link is
both a deliverability liability and a trust problem. Standard practice is no
link in the first touch. This pattern appears in all four emails in all three
lanes.

Note: the cold-outreach SOP explicitly says every email closes with the
`/hello` link and that the link structure must never be edited. The rewrite
below keeps the link and its UTM structure exactly as specified but moves it to
email 3 only. **This is a deliberate departure from the SOP and needs your
sign-off** — if the SOP rule stands, the link goes back in every email and this
recommendation is void.

### 2.4 The opener is hollow flattery

> "I came across {{company}} recently and wanted to reach out personally. What
> you've built is genuinely impressive, and I can see the practice is moving."

Applied to a four-person therapy practice, "what you've built is genuinely
impressive" reads as exactly what it is — a line written once and sent to
everyone. It signals template in the first sentence, which is where the
reader decides whether to keep going. "Personally" is doing no work.

### 2.5 It is about Ricardo, not the reader

Email 1 paragraph 4 is a straight services pitch: "I work with founders like
you to identify where the manual work lives, build systems that remove it, and
create the kind of operational clarity that…" Three of four paragraphs open
with "I."

### 2.6 Subject lines write cheques the body doesn't cash

- **"A question for you, {{first_name}}"** — there is no question in the email.
  A subject that promises something the body doesn't deliver is both a trust
  cost and a spam-filter pattern.
- **"The quiet cost most founders never calculate"** — clickbait register, and
  long.
- "The hire that didn't fix it" is genuinely good. Keep it.

### 2.7 The breakup email doesn't ask anything either

Email 4 is the highest-reply-potential touch in any cold sequence, because a
graceful exit gives people a reason to respond. This one exits with a link.

### 2.8 Smaller items

- **Voice slips from "I" to "we"** in email 3 ("Many practices we work with").
  Pick one. For a solo consultant, "I" is stronger.
- **Pain is asserted, not asked.** "But the founder is still the one holding
  too many things together" tells a stranger what their life is like. Asking
  invites a correction, which is a reply.
- **The full title block** ("AI Operations Consultant & Fractional COO, Ricardo
  Cruz Consulting") on all four emails reinforces "this is a sales email." A
  first-name sign-off outperforms it.

---

## 3. Rewritten sequence — Mental Health lane

Cadence unchanged in shape, tightened slightly: Day 0, 4, 11, 19.
Sender: ricardo@ricardocruz.io. Sign-off is first name only.

Writing rules from the SOP are respected: no "it's not X, it's Y" constructs,
maximum one em dash per email, no buzzwords, calm and observational tone.

### Email 1 — Day 0
**Subject:** {{company}}'s intake process

> Hi {{first_name}},
>
> Most therapy practice owners I speak with lose 10 to 15 hours a week to
> scheduling, insurance verification, and session notes — work that lands on
> them because no system owns it.
>
> Is that roughly true at {{company}}, or have you got that handled already?
>
> Ricardo

*51 words. One question, answerable in four words. No link. The "or have you
got that handled" gives an easy out, which raises reply rates rather than
lowering them.*

### Email 2 — Day 4
**Subject:** The hire that didn't fix it

> Hi {{first_name}},
>
> The usual first move here is hiring — a front desk coordinator, a billing
> specialist. It rarely works, because hiring into a manual process just adds
> hands to it.
>
> One practice I worked with replaced their intake paperwork with a single form
> that triggered onboarding automatically. About 14 hours a week came back to
> the team. No new hire.
>
> Worth me showing you where yours is going?
>
> Ricardo

*76 words. Keeps the strongest existing subject line and the strongest existing
story, cut to its bones.*

### Email 3 — Day 11
**Subject:** The math on 15 hours

> Hi {{first_name}},
>
> Rough math: 15 hours a week of manual admin at $75 an hour runs about $58,500
> a year. That cost never lands on a P&L, which is why it goes unnoticed for
> years.
>
> I built a short calculator so you can run your own numbers:
> ricardocruz.io/hello
>
> If the figure looks wrong for {{company}}, tell me and I'll stop guessing.
>
> Ricardo

*70 words. The one link in the sequence, at the touch where trust is highest.
Link text and UTM structure unchanged from spec
(`utm_campaign=mental_health&utm_content=email3`). Still closes on a reply ask,
not the click.*

### Email 4 — Day 19
**Subject:** Closing the loop

> Hi {{first_name}},
>
> I haven't heard back, so I'll assume the timing isn't right and leave it here.
>
> One thing before I do — was it timing, or is operations simply not the
> bottleneck at {{company}} right now? Either answer is genuinely useful to me.
>
> Ricardo

*54 words. A real question at the exit. This touch typically produces the
highest reply rate in the sequence.*

---

## 4. Lane swaps

Structure is identical across lanes. Only the email 1 pain line changes, plus
one line in email 2 for Wellness/Fitness. This mirrors how the current
templates are organised.

### Medical Practice
Email 1, pain line:

> Most practice owners I speak with lose 10 to 15 hours a week to patient
> intake, billing, and supply coordination — work that lands on them because no
> system owns it.

UTM: `utm_campaign=medical_practice`

### Wellness / Fitness
Email 1, pain line:

> Most studio owners I speak with lose 10 to 15 hours a week to scheduling,
> client onboarding, and membership tracking — work that lands on them because
> no system owns it.

Email 2, opening line:

> The usual first move here is hiring — a front desk lead, a part-time admin.
> It rarely works, because hiring into a manual process just adds hands to it.

UTM: `utm_campaign=wellness_fitness`. Use "business" rather than "practice"
throughout.

---

## 5. Recommendations before relaunch

1. **Get sign-off on the link change** (section 2.3). It contradicts a standing
   SOP rule and is the only change here that does.
2. **Raise volume before drawing conclusions.** Target 300+ contacts per lane.
   At current volume the next campaign will be as unreadable as the last.
3. **Test one variable, not two.** The V2 A/B changed the entire angle
   (Founder Dependency vs Admin Capacity) across every email. Test subject
   lines or the email 1 pain line, holding everything else fixed.
4. **Check inbox placement** before relaunch, given the spam blocks and
   Variant A's 7.7% open rate.
5. **Measure replies, not opens.** Apollo's open tracking is filtering bot
   traffic and reporting 100% unfiltered open rates on three sequences. Reply
   rate is the only trustworthy number.
6. **Three empty V2 sequences are sitting in Apollo** (created 2026-07-29,
   inactive, zero sends): Mental Health, Medical Practice, and Wellness Fitness
   "(Stage 2, A/B v2)". Their bodies can't be read through the Apollo
   connector. Confirm what's in them before creating anything new, or they'll
   accumulate as clutter.
