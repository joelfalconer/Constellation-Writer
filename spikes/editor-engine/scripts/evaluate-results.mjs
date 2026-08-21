import { readFile } from "node:fs/promises";
import process from "node:process";

const path = process.argv[2];
if (!path) throw new Error("usage: node evaluate-results.mjs <result.json>");
const report = JSON.parse(await readFile(path, "utf8"));
const cm = report.results.codemirror6;
const pm = report.results.prosemirror;
const failures = [];
if (!cm.canonical_source_exact_at_mount) failures.push("CodeMirror did not preserve canonical source at mount");
if (!cm.overlay_removal_preserves_source) failures.push("CodeMirror decoration toggle changed source");
if (!cm.undo_round_trip_exact) failures.push("CodeMirror undo failed exact source round trip");
if (cm.return_token_scroll_drift_px > 4) failures.push(`CodeMirror return token scroll drift ${cm.return_token_scroll_drift_px}px`);
for (const [metric, value] of Object.entries(cm.metrics_ms)) {
  if (!Number.isFinite(value)) failures.push(`CodeMirror ${metric} is not finite`);
}
for (const [metric, value] of Object.entries(pm.metrics_ms)) {
  if (!Number.isFinite(value)) failures.push(`ProseMirror ${metric} is not finite`);
}
if (failures.length) {
  console.error(JSON.stringify({ verdict: "fail", failures }, null, 2));
  process.exit(1);
}
console.log(JSON.stringify({
  verdict: "pass_harness_hard_gates",
  code_mirror_budget_observations: cm.metrics_ms,
  prose_mirror_budget_observations: pm.metrics_ms,
  prose_mirror_exact_source_round_trip: pm.source_fidelity_fixture_exact_round_trip,
  reminder: "real IME, assistive technology, physical high contrast, native clipboard/drag and six-hour fatigue remain unmeasured"
}, null, 2));
