import { EditorState, StateEffect, StateField } from "@codemirror/state";
import { EditorView, Decoration, keymap } from "@codemirror/view";
import { defaultKeymap, history, historyKeymap, undo, redo } from "@codemirror/commands";
import { markdown } from "@codemirror/lang-markdown";
import { LONGFORM_FIXTURE, FIXTURE_WORD_COUNT } from "./fixture.js";
import { measureFrame, p95, installPaneToggle, dispatchSyntheticComposition } from "./shared.js";

const setRevisionDecorations = StateEffect.define();
const revisionField = StateField.define({
  create: () => Decoration.none,
  update(value, transaction) {
    let next = value.map(transaction.changes);
    for (const effect of transaction.effects) {
      if (effect.is(setRevisionDecorations)) next = effect.value;
    }
    return next;
  },
  provide: (field) => EditorView.decorations.from(field)
});

function revisionDecorations(doc) {
  const max = doc.length;
  const firstFrom = Math.min(100, max);
  const firstTo = Math.min(firstFrom + 48, max);
  const secondFrom = Math.min(126, max);
  const secondTo = Math.min(secondFrom + 64, max);
  const decorations = [];
  if (firstTo > firstFrom) decorations.push(Decoration.mark({ class: "revision-a", attributes: { "data-revision": "comment" } }).range(firstFrom, firstTo));
  if (secondTo > secondFrom) decorations.push(Decoration.mark({ class: "revision-b", attributes: { "data-revision": "patch" } }).range(secondFrom, secondTo));
  return Decoration.set(decorations, true);
}

const proseTheme = EditorView.theme({
  "&": { height: "100%", fontSize: "18px", backgroundColor: "Canvas", color: "CanvasText" },
  ".cm-scroller": { fontFamily: "Georgia, 'Times New Roman', serif", lineHeight: "1.55", overflow: "auto" },
  ".cm-content": { maxWidth: "66ch", margin: "0 auto", padding: "64px 40px 40vh", caretColor: "CanvasText" },
  ".cm-line": { padding: "0" },
  ".revision-a": { textDecoration: "underline", textDecorationThickness: "2px" },
  ".revision-b": { outline: "1px dotted currentColor" },
  "&.cm-focused": { outline: "none" }
});

export function mountCodeMirror(host) {
  let mode = "draft";
  let typewriter = false;
  const state = EditorState.create({
    doc: LONGFORM_FIXTURE,
    extensions: [
      history(),
      keymap.of([...defaultKeymap, ...historyKeymap]),
      markdown(),
      revisionField,
      proseTheme,
      EditorView.lineWrapping,
      EditorView.contentAttributes.of({
        role: "textbox",
        "aria-label": "Manuscript editor",
        "aria-multiline": "true",
        spellcheck: "true"
      })
    ]
  });
  const view = new EditorView({ state, parent: host });
  const togglePane = installPaneToggle();

  function setMode(next) {
    mode = next;
    document.body.dataset.mode = next;
    view.dispatch({ effects: setRevisionDecorations.of(next === "revise" ? revisionDecorations(view.state.doc) : Decoration.none) });
  }

  function setTypewriter(next) {
    typewriter = next;
    if (typewriter) view.dispatch({ effects: EditorView.scrollIntoView(view.state.selection.main.head, { y: "center" }) });
  }

  function captureReturnToken() {
    return {
      anchor: view.state.selection.main.anchor,
      head: view.state.selection.main.head,
      scrollTop: view.scrollDOM.scrollTop,
      mode,
      typewriter
    };
  }

  function restoreReturnToken(token) {
    setMode(token.mode);
    typewriter = token.typewriter;
    view.dispatch({ selection: { anchor: token.anchor, head: token.head } });
    view.scrollDOM.scrollTop = token.scrollTop;
  }

  function insertText(text) {
    const head = view.state.selection.main.head;
    view.dispatch({ changes: { from: head, to: head, insert: text }, selection: { anchor: head + text.length } });
    if (typewriter) view.dispatch({ effects: EditorView.scrollIntoView(head + text.length, { y: "center" }) });
  }

  function moveCursor(delta) {
    const head = view.state.selection.main.head;
    const next = Math.max(0, Math.min(view.state.doc.length, head + delta));
    view.dispatch({ selection: { anchor: next } });
  }

  function selectSpan(length = 8) {
    const head = view.state.selection.main.head;
    const from = Math.max(0, Math.min(view.state.doc.length - 1, head));
    const to = Math.min(view.state.doc.length, from + length);
    view.dispatch({ selection: { anchor: from, head: to } });
  }

  async function runSyntheticBenchmark(iterations = 120) {
    setMode("draft");
    const canonicalBefore = view.state.doc.toString();
    const overlayBefore = canonicalBefore;
    setMode("revise");
    const overlaySourceExact = view.state.doc.toString() === overlayBefore;
    setMode("draft");

    const undoBefore = view.state.doc.toString();
    insertText("¤");
    const undoApplied = undo(view);
    const undoRoundTripExact = undoApplied && view.state.doc.toString() === undoBefore;
    redo(view);
    undo(view);

    view.scrollDOM.scrollTop = Math.max(0, Math.floor((view.scrollDOM.scrollHeight - view.scrollDOM.clientHeight) / 2));
    await new Promise(requestAnimationFrame);
    const token = captureReturnToken();
    const paneBefore = view.scrollDOM.scrollTop;
    togglePane();
    await new Promise(requestAnimationFrame);
    restoreReturnToken(token);
    await new Promise(requestAnimationFrame);
    const paneAfter = view.scrollDOM.scrollTop;

    const keystrokes = [];
    for (let i = 0; i < iterations; i += 1) keystrokes.push(await measureFrame(() => insertText("x")));
    const cursor = [];
    for (let i = 0; i < iterations; i += 1) cursor.push(await measureFrame(() => moveCursor(i % 2 === 0 ? -1 : 1)));
    const selection = [];
    for (let i = 0; i < iterations; i += 1) selection.push(await measureFrame(() => selectSpan((i % 12) + 1)));

    const pane = [];
    for (let i = 0; i < 40; i += 1) pane.push(await measureFrame(() => togglePane()));

    const composition = dispatchSyntheticComposition(view.contentDOM);
    const semantics = {
      role: view.contentDOM.getAttribute("role"),
      aria_multiline: view.contentDOM.getAttribute("aria-multiline"),
      contenteditable: view.contentDOM.getAttribute("contenteditable")
    };

    return {
      engine: "codemirror6",
      fixture_words: FIXTURE_WORD_COUNT,
      canonical_source_exact_at_mount: canonicalBefore === LONGFORM_FIXTURE,
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
    engine: "codemirror6",
    ready: true,
    view,
    setMode,
    setTypewriter,
    captureReturnToken,
    restoreReturnToken,
    togglePane,
    getSource: () => view.state.doc.toString(),
    runSyntheticBenchmark
  };
}
