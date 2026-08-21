# Benchmark Dossier: Drafts

```yaml
status: refreshed_candidate
updated_at: 2026-08-17
historical_source_basis: [SRC-DR-001, EU-004]
current_source_basis:
  - SRC-OFFICIAL-DRAFTS-START-20260817
  - SRC-OFFICIAL-DRAFTS-ACTIONS-20260817
  - SRC-OFFICIAL-DRAFTS-WORKSPACES-20260817
  - SRC-OFFICIAL-DRAFTS-TAGS-20260817
current_evidence_unit: EU-019
validation_state: machine_checked_current_docs
historical_locator_status: unresolved_source_unavailable
```

## Historical report finding

The inherited Deep Research ledger identifies Drafts as the text-first capture, routing, and automation benchmark. Its exact `SRC-DR-001` span cannot be backfilled safely because the final report attachment is unavailable in the current run.

## Current official product state

Current Drafts documentation establishes that:

- Drafts is a plain-text editor with Markdown syntax highlighting and other markup modes;
- the Draft List retrieves, filters, and organizes past drafts;
- the Action List contains explicit commands that manipulate text or send it to other apps/services;
- actions can range from simple text helpers to scripted integrations;
- Workspaces save search, tag filters, display/sort options, and action-group context for different activities;
- tags, including scoped tags, can represent workflow state and priorities.

These sources establish a capture-and-route architecture. They do not prove launch speed, cognitive effort, reliability, or whether professional writers prefer Drafts to manuscript-centered applications.

## Benchmark interpretation

Drafts demonstrates a useful separation between **text capture**, **text organization**, and **explicit actions**. The transferable lesson for Constellation is not to become an action launcher, but to make commands and routing operations explicit, keyboard-accessible, and reversible while preserving a low-friction path into text.

## Atomic affordances to benchmark

- new-draft entry and immediate editor focus;
- Draft List retrieval and filtering;
- action invocation and post-action state;
- workspace switching and saved context;
- tags as lightweight workflow state;
- external keyboard action triggering.

## Borrow / reject / test

**Borrow candidate:** text-first entry, explicit action grammar, saved retrieval contexts, and keyboard-triggered routing.

**Reject candidate:** requiring automation configuration for ordinary project writing or allowing actions to bypass canonical mutation/recovery contracts.

**Test in Constellation:** whether the command palette, quick capture, and import/routing flows can approach Drafts-style explicitness without competing with manuscript structure or governed writes.

## Evidence table

| Claim | Basis | Locator | Validation |
|---|---|---|---|
| Historical synthesis: text-first capture, routing, automation are Drafts' strongest benchmark contribution | EU-004 / SRC-DR-001 | unresolved: final report unavailable | unreviewed historical assertion |
| Plain-text editor plus Draft List and Action List | EU-019 / SRC-OFFICIAL-DRAFTS-START-20260817 | `Getting Started` | machine checked |
| Actions manipulate/output text and may include scripted integrations | EU-019 / SRC-OFFICIAL-DRAFTS-ACTIONS-20260817 | `Actions` | machine checked |
| Workspaces save filters and app/action context | EU-019 / SRC-OFFICIAL-DRAFTS-WORKSPACES-20260817 | `Workspaces` | machine checked |
| Tags can encode workflow state and filter workspaces | EU-019 / SRC-OFFICIAL-DRAFTS-TAGS-20260817 | `Flags & Tagging` | machine checked |

## Remaining gaps

- Exact `SRC-DR-001` span.
- Measured launch/capture latency.
- Data/storage/recovery characteristics under failure.
- Accessibility and long-session behavior.
- Switching evidence from writers who use Drafts alongside manuscript tools.
