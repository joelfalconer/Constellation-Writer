# Navigation and Return Contract v0.1

## Principle

Every summoned operation must preserve a reliable path back to the sentence.

## Return token

```yaml
return_token:
  project_id: prj_...
  manuscript_id: ms_...
  placement_id: nd_...
  sheet_id: sh_...
  revision_id: rev_...
  selection_anchor: optional_hybrid_anchor
  cursor_offset_hint: integer
  scroll_anchor: string
  editor_mode: draft|revise
  pane_state: {}
  created_at: timestamp
```

Return tokens are local user state. They are not project canon.

## Operations requiring return tokens

- quick open;
- project search;
- entity or claim inspection;
- compile preview;
- patch review;
- snapshot comparison;
- conflict resolution;
- external file reveal;
- source inspection.

## Return behavior

1. Reopen the originating Sheet and revision context.
2. Resolve the selection anchor against current text.
3. Restore cursor and scroll when safe.
4. If the Sheet changed, show the nearest confident anchor and explain drift.
5. If the Sheet no longer exists, offer history, replacement, or manuscript parent.

## Hard failures

- a pane toggle moves the active sentence unexpectedly;
- search clears the query before return;
- compile preview forgets the originating location;
- patch review applies and lands the writer at project root;
- stale anchors silently select unrelated text.
