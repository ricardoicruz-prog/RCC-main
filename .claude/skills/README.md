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

## Lessie Skills (2) — third-party paid service

`people-search` (contact/company enrichment, lead sourcing) and `lessie-email`
(multi-provider email send/manage, bulk campaigns). Unlike the collections above,
these are **wrappers around Lessie, a commercial third-party service** and are
**not self-contained**:

- Require a Lessie account (app.lessie.ai) and browser OAuth login.
- **Cost real money** — credit-based (e.g. a people search ~20 credits, phone
  unlock ~8 credits). Both skills are built to confirm cost before spending.
- `people-search` auto-installs a global CLI (`@lessie/cli`) or an MCP server when
  triggered; `lessie-email` requires the Lessie MCP server and bound email accounts.
- Handle personal contact data and can send email on your behalf — use in
  compliance with GDPR / CAN-SPAM. Ricardo is responsible for lawful use.

Source: https://github.com/LessieAI/lessie-skill (no explicit license file in repo).
