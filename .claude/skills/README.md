# RCC Custom Skills

Custom skill collections for Ricardo Cruz Consulting (RCC). Skills load
automatically when a task matches a skill's description — no manual setup is
required beyond having this directory in the project.

## Brand Building Skills (29)

Covers brand strategy, naming, identity, voice, positioning, messaging,
auditing, guidelines, launch, and marketing channels. `brand-context` is the
foundation skill — every other brand skill reads it first, so run it once per
client to capture identity, audience, and positioning.

Source: https://github.com/arnabbagxd/Brand-building-skills (MIT License — see `LICENSE`).

## Marketing Skills (25)

Growth and conversion skills for technical marketers and founders: CRO
(page/form/popup/onboarding/paywall/signup), copywriting and copy-editing,
SEO (audit, programmatic, schema markup), paid ads, email sequences, pricing
strategy, referral programs, analytics tracking, A/B testing, and more.
`product-marketing-context` is the foundation skill for this set — run it first
to capture product, audience, and positioning that the other skills build on.

Several of these skills link to `../tools/` (a tool/integration reference
registry that ships alongside them under `.claude/tools/`).

Source: https://github.com/ayrshare/marketingskills (MIT License — see `LICENSE-marketingskills`).

## Cold Outbound Skills (28)

End-to-end cold email: strategy, sending infrastructure, list building, copy,
and iteration. `cold-email-kickoff` is the entry point — it orchestrates
`icp-onboarding` → `lead-magnet-brainstorm` → `campaign-strategy` into a single
`campaign-plan.md`. For cold email *structure* specifically, the relevant
skills are `campaign-copywriting` (direction → subject → body → final YAML),
`smartlead-spintax`, `spam-word-checker`, and
`cold-email-starter-kit/references/04-sequence-structure.md`.

The five tracks:

- **Strategy** — `cold-email-kickoff`, `icp-onboarding`, `lead-magnet-brainstorm`,
  `campaign-strategy`, `campaign-copywriting`
- **Infrastructure** — `zapmail-domain-setup-public`, `smartlead-inbox-manager`,
  `email-deliverability-audit`, `deliverability-incident-response`
- **List building** — `prospeo-full-export`, `prospeo-search-api`,
  `blitz-list-builder`, `google-maps-list-builder`, `disco-like`,
  `competitor-engagers`, `icp-prompt-builder`, `list-quality-scorecard`
- **Copy & send** — `cold-email-starter-kit`, `spam-word-checker`,
  `smartlead-spintax`, `smartlead-api`, `smartlead-campaign-upload-public`
- **Iterate & automate** — `positive-reply-scoring`, `experiment-design`,
  `auto-research-public`, `personalization-subagent-pattern`,
  `deliverability-test-public`, `cold-email-weekly-rhythm`

Unlike the brand and marketing sets, several of these skills run real code
against paid third-party APIs. They are inert until you supply keys:

1. Copy `cold-outbound.env.example` to the project root as `.env` (or merge it
   into the existing `.env`) and fill in only the keys you need. The minimum
   viable set for a first campaign is Dynadot + Zapmail + Prospeo + Smartlead.
2. Install the TypeScript runner: `npm install -g tsx`.
3. Verify with
   `npx tsx .claude/skills/cold-email-starter-kit/scripts/verify-credentials.ts`.

Skills that write client data (ICP profiles, experiment logs, reply scores)
write to `profiles/<business-slug>/` at the project root, which is gitignored —
it holds client information and should stay out of version control.

Upstream paths were rewritten on install: the source repo assumes a
`~/cold-email-ai-skills` clone, so script and profile references were repointed
to `.claude/skills/` and `profiles/`. Two upstream references are dangling and
were left as-is: `icp-onboarding` mentions a `references/example-profiles/`
directory and `icp-prompt-builder` mentions a `scripts/score-batch.ts` — neither
ships in the source repo.

Source: https://github.com/growthenginenowoslawski/coldoutboundskills
(MIT License — see `LICENSE-coldoutboundskills`).
