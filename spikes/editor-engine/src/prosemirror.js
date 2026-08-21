import { EditorState, Plugin, PluginKey, TextSelection } from "prosemirror-state";
import { EditorView, Decoration, DecorationSet } from "prosemirror-view";
import { history, undo, redo } from "prosemirror-history";
import { keymap } from "prosemirror-keymap";
import { baseKeymap } from "prosemirror-commands";
import { defaultMarkdownParser, defaultMarkdownSerializer } from "prosemirror-markdown";
import { LONGFORM_FIXTURE, FIXTURE_WORD_COUNT, SOURCE_FIDELITY_FIXTURE } from "./fixture.js";
import { measureFrame, p95, installPaneToggle, dispatchSyntheticComposition } from "./shared.js";

const revisionKey = new PluginKey("revision-decorations");
function buildDecorations(doc) {
  const marks = [];
  let found = 0;
  doc.descendants((node, pos) => {
    if (!node.isText || found >= 2) return found < 2;
    const length = Math.min(node.nodeSize, found === 0 ? 48 : 64);
    if (length > 1) {
      marks.push(Decoration.inline(pos, pos + length, { class: found === 0 ? "revision-a" : "revision-b", "data-revision": found === 0 ? "comment" : "patch" }));
      found += 1;
    }
    return found < 2;
  });
  return DecorationSet.create(doc, marks);
}
const revisionPlugin = new Plugin({
  key: revisionKey,
  state: {
    init: () => DecorationSet.empty,
    apply(transaction, value, _oldState, newState) {
      let next = value.map(transaction.mapping, newState.doc);
      const requested = transaction.getMeta(revisionKey);
      if (requested === "on") next = buildDecorations(newState.doc);
      if (requested === "off") next = DecorationSet.empty;
      return next;
    }
  },
  props: {
    decorations(state) {
      return revisionKey.getState(state);
    },
    attributes: {
      role: "textbox",
      "aria-label": "Manuscript editor",
      "aria-multiline": "true",
      spellcheck: "true"
    }
  }
});

function parseMarkdown(source) {
  return defaultMarkdownParser.parse(source);
}

export function mountProseMirror(host) {
  let mode = "draft";
  let typewriter = false;
  const doc = parseMarkdown(LONGFORM_FIXTURE);
  const state = EditorState.create({ doc, plugins: [history(), keymap(baseKeymap), revisionPlugin] });
  const view = new EditorView(host, { state });
  view.dom.classList.add("prosemirror-prose");
  const togglePane = installPaneToggle();
  const scrollContainer = document.querySelector("#editor-frame");
  const initialSerialized = defaultMarkdownSerializer.serialize(view.state.doc) + "\n";
  const fidelityRoundTrip = defaultMarkdownSerializer.serialize(parseMarkdown(SOURCE_FIDELITY_FIXTURE)) + "\n";

  function setMode(next) {
    mode = next;
    document.body.dataset.mode = next;
    view.dispatch(view.state.tr.setMeta(revisionKey, next === "revise" ? "on" : "off"));
  }

  function setTypewriter(next) {
    typewriter = next;
    if (typewriter) view.dispatch(view.state.tr.scrollIntoView());
  }

  function captureReturnToken() {
    return {
      anchor: view.state.selection.anchor,
      head: view.state.selection.head,
      scrollTop: scrollContainer?.scrollTop ?? 0,
      mode,
      typewriter
    };
  }

  function restoreReturnToken(token) {
    setMode(token.mode);
    typewriter = token.typewriter;
    const max = view.state.doc.content.size;
    const anchor = Math.max(1, Math.min(max, token.anchor));
    const head = Math.max(1, Math.min(max, token.head));
    view.dispatch(view.state.tr.setSelection(TextSelection.create(view.state.doc, anchor, head)));
    if (scrollContainer) scrollContainer.scrollTop = token.scrollTop;
  }

  function insertText(text) {
    view.dispatch(view.state.tr.insertText(text).scrollIntoView());
  }

  function moveCursor(delta) {
    const max = view.state.doc.content.size;
    const head = view.state.selection.head;
    const next = Math.max(1, Math.min(max, head + delta));
    view.dispatch(view.state.tr.setSelection(TextSelection.create(view.state.doc, next)));
  }

  function selectSpan(length = 8) {
    const max = view.state.doc.content.size;
    const from = Math.max(1, Math.min(max, view.state.selection.head));
    const to = Math.max(from, Math.min(max, from + length));
    view.dispatch(view.state.tr.setSelection(TextSelection.create(view.state.doc, from, to)));
  }

  async function runSyntheticBenchmark(iterations = 120) {
    setMode("draft");
    const sourceAtMount = initialSerialized;
    const sourceBeforeOverlay = defaultMarkdownSerializer.serialize(view.state.doc) + "\n";
    setMode("revise");
    const overlaySourceExact = defaultMarkdownSerializer.serialize(view.state.doc) + "\n" === sourceBeforeOverlay;
    setMode("draft");

    const undoBefore = defaultMarkdownSerializer.serialize(view.state.doc) + "\n";
    insertText("¤");
    const undoApplied = undo(view.state, view.dispatch.bind(view));
    const undoRoundTripExact = undoApplied && defaultMarkdownSerializer.serialize(view.state.doc) + "\n" === undoBefore;
    redo(view.state, view.dispatch.bind(view));
    undo(view.state, view.dispatch.bind(view));

    if (scrollContainer) scrollContainer.scrollTop = Math.max(0, Math.floor((scrollContainer.scrollHeight - scrollContainer.clientHeight) / 2));
    await new Promise(requestAnimationFrame);
    const token = captureReturnToken();
    const paneBefore = scrollContainer?.scrollTop ?? 0;
    togglePane();
    await new Promise(requestAnimationFrame);
    restoreReturnToken(token);
    await new Promise(requestAnimationFrame);
    const paneAfter = scrollContainer?.scrollTop ?? 0;

    const keystrokes = [];
    for (let i = 0; i < iterations; i += 1) keystrokes.push(await measureFrame(() => insertText("x")));
    const cursor = [];
    for (let i = 0; i < iterations; i += 1) cursor.push(await measureFrame(() => moveCursor(i % 2 === 0 ? -1 : 1)));
    const selection = [];
    for (let i = 0; i < iterations; i += 1) selection.push(await measureFrame(() => selectSpan((i % 12) + 1)));
    const pane = [];
    for (let i = 0; i < 40; i += 1) pane.push(await measureFrame(() => togglePane()));

    const composition = dispatchSyntheticComposition(view.dom);
    const semantics = {
      role: view.dom.getAttribute("role"),
      aria_multiline: view.dom.getAttribute("aria-multiline"),
      contenteditable: view.dom.getAttribute("contenteditable")
    };

    return {
      engine: "prosemirror",
      fixture_words: FIXTURE_WORD_COUNT,
      canonical_source_exact_at_mount: sourceAtMount === LONGFORM_FIXTURE,
      source_fidelity_fixture_exact_round_trip: fidelityRoundTrip === SOURCE_FIDELITY_FIXTURE,
      overlay_removal_preserves_source: overlaySourceExact,
      undo_round_trip_exact: undoRoundTripExact,
      return_token_scroll_drift_px: Math.abs(paneAfter - paneBefore),
      synthetic_composition: composition,
      dom_accessibility_semantics: semantics,
      metrics_ms: {
        keystroke_p95: p95(keystrokes),
        cursor_p95: p95(cursor),
        selection_p95: p95(selection),
        pane_toggle_p95: p95(pane)
      },
      samples: { keystrokes, cursor, selection, pane }
    };
  }

  setMode("draft");
  return {
    engine: "prosemirror",
    ready: true,
    view,
    setMode,
    setTypewriter,
    captureReturnToken,
    restoreReturnToken,
    togglePane,
    getSource: () => defaultMarkdownSerializer.serialize(view.state.doc) + "\n",
    runSyntheticBenchmark
  };
}
