export function p95(values) {
  if (!values.length) return 0;
  const sorted = [...values].sort((a, b) => a - b);
  return sorted[Math.min(sorted.length - 1, Math.ceil(sorted.length * 0.95) - 1)];
}

export function nextFrame() {
  return new Promise((resolve) => requestAnimationFrame(() => resolve()));
}

export async function measureFrame(fn) {
  const start = performance.now();
  fn();
  await nextFrame();
  return performance.now() - start;
}

export function installPaneToggle() {
  let hidden = false;
  return () => {
    const before = window.scrollY;
    hidden = !hidden;
    document.body.classList.toggle("panes-hidden", hidden);
    return { before, hidden };
  };
}

export function dispatchSyntheticComposition(target) {
  const events = [
    new CompositionEvent("compositionstart", { data: "" }),
    new CompositionEvent("compositionupdate", { data: "日本" }),
    new CompositionEvent("compositionend", { data: "日本語" })
  ];
  for (const event of events) target.dispatchEvent(event);
  return { dispatched: events.length, proof_level: "synthetic_dom_event_only" };
}
