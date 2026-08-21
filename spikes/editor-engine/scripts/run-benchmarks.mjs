import { chromium } from "playwright";
import { spawn } from "node:child_process";
import { mkdir, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import process from "node:process";

const platformArg = process.argv.find((arg) => arg.startsWith("--platform="));
const platform = platformArg ? platformArg.split("=")[1] : process.platform;
const port = 4174;
const spikeRoot = fileURLToPath(new URL("..", import.meta.url));
const viteBin = fileURLToPath(new URL("../node_modules/vite/bin/vite.js", import.meta.url));
const server = spawn(process.execPath, [viteBin, "preview", "--host", "127.0.0.1", "--port", String(port)], {
  cwd: spikeRoot,
  stdio: ["ignore", "pipe", "pipe"]
});

async function waitForServer() {
  const url = `http://127.0.0.1:${port}/`;
  for (let i = 0; i < 80; i += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) return;
    } catch {}
    await new Promise((resolve) => setTimeout(resolve, 250));
  }
  throw new Error("Vite preview did not become ready");
}

async function runEngine(browser, engine) {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  await page.goto(`http://127.0.0.1:${port}/?engine=${engine}`, { waitUntil: "networkidle" });
  await page.waitForFunction(() => window.editorSpike?.ready === true);
  const result = await page.evaluate(async () => window.editorSpike.runSyntheticBenchmark(120));
  await page.emulateMedia({ forcedColors: "active", reducedMotion: "reduce" });
  result.synthetic_accessibility_media = await page.evaluate(() => ({
    forced_colors_active: matchMedia("(forced-colors: active)").matches,
    reduced_motion_reduce: matchMedia("(prefers-reduced-motion: reduce)").matches
  }));
  await page.close();
  return result;
}

let browser;
try {
  await waitForServer();
  browser = await chromium.launch({ headless: true });
  const codemirror = await runEngine(browser, "codemirror6");
  const prosemirror = await runEngine(browser, "prosemirror");
  const report = {
    schema: "cw_editor_engine_spike_result_v1",
    platform,
    runner: "github_hosted_or_equivalent",
    browser: await browser.version(),
    measured_at: new Date().toISOString(),
    evidence_limits: [
      "synthetic_browser_events_are_not_real_IME_candidate_window_evidence",
      "DOM_accessibility_semantics_are_not_screen_reader_traversal_evidence",
      "forced-colors_emulation_is_not_physical_OS_high_contrast_validation",
      "six_hour_fatigue_protocol_not_executed_in_CI",
      "native_clipboard_drag_drop_and_platform_text_services_require_physical_assay"
    ],
    results: { codemirror6: codemirror, prosemirror }
  };
  await mkdir(new URL("../results/raw/", import.meta.url), { recursive: true });
  const output = new URL(`../results/raw/${platform}-editor-engine.json`, import.meta.url);
  await writeFile(output, JSON.stringify(report, null, 2) + "\n", "utf8");
  console.log(JSON.stringify(report, null, 2));
} finally {
  if (browser) await browser.close();
  server.kill();
}
