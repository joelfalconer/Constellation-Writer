import test from "node:test";
import assert from "node:assert/strict";
import { buildLongformFixture, LONGFORM_FIXTURE } from "../src/fixture.js";

function p95(values) {
  const sorted = [...values].sort((a, b) => a - b);
  return sorted[Math.min(sorted.length - 1, Math.ceil(sorted.length * 0.95) - 1)];
}

test("fixture is deterministic and exceeds the 50k target including mixed-script additions", () => {
  assert.equal(buildLongformFixture(), LONGFORM_FIXTURE);
  assert.ok(LONGFORM_FIXTURE.split(/\s+/u).length >= 50000);
  assert.match(LONGFORM_FIXTURE, /日本語/);
  assert.match(LONGFORM_FIXTURE, /العربية/);
  assert.match(LONGFORM_FIXTURE, /עברית/);
});

test("p95 helper selects the 95th percentile sample", () => {
  const samples = Array.from({ length: 100 }, (_, index) => index + 1);
  assert.equal(p95(samples), 95);
});
