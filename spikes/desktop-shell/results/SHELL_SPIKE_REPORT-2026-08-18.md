# Desktop Shell Decision Spike Report

**Run:** `CW-F1-SHELL-SPIKE-003`  
**Issue:** #3  
**Measured head:** `d9991c9245caf689de7ebfa4eb0a735f41a8a7a4`  
**Desktop-spike workflow:** `32085957984`  
**Foundation validation:** `32085957973`  
**Decision:** select Electron 43.2.0 for the F2 desktop scaffold, with physical IME/accessibility vetoes carried forward.

## 1. What was actually compared

The two controls use the same Vite/CodeMirror renderer and exactly the same deterministic 50,000-word fixture. Each control implements a deliberately narrow shell boundary for native open/save dialogs, project-root selection, filesystem watching, native menu/shortcut, clipboard, drag/drop plumbing, crash/restart marker, and a project-root-restricted atomic-write placeholder.

The Electron control uses a sandboxed renderer with `contextIsolation`, no renderer Node integration, blocked arbitrary navigation, a narrow preload API, and main-process filesystem operations. The Tauri control exposes a narrow Rust command set; frontend capabilities do not receive general filesystem permission.

Both implementations have deterministic project-root path traversal and symlink-escape negative tests.

## 2. Automated result

All four final matrix jobs passed:

- macOS + Electron: pass
- Windows + Electron: pass
- macOS + Tauri: pass
- Windows + Tauri: pass

Both the shared renderer build and shell-specific boundary tests passed on both target operating systems. Both packaged controls produced a runtime-ready report on GitHub-hosted runners.

The Tauri spike initially exposed fixture/package setup defects, first a missing default PNG and then missing platform bundle icons. Those were repaired in the spike. They are recorded as build-tooling friction, not as a product-runtime veto.

## 3. Measurements

| Platform | Shell | Shell → renderer ready | 50k editor init | first paint | best-effort process-tree RSS | package/output measurement |
|---|---:|---:|---:|---:|---:|---:|
| macOS | Electron | 1,889.843 ms | 391.2 ms | 700.2 ms | 403,984 KB | 479.049 MiB |
| macOS | Tauri | 4,884.459 ms | 119.0 ms | 344.0 ms | 96,544 KB | 11.123 MiB |
| Windows | Electron | 971.012 ms | 159.4 ms | 431.5 ms | 295,316 KB | 347.958 MiB |
| Windows | Tauri | 12,525.568 ms | 265.1 ms | 629.2 ms | 361,668 KB | 2.194 MiB |

These are one hosted-runner observation per shell/platform and are not production performance budgets.

### Measurement caveats

The package figures are intentionally **not** treated as an apples-to-apples winner metric. The Windows Electron measurement is an unpacked packager output tree, while the Windows Tauri measurement is the NSIS distribution output. Tauri also relies on an OS WebView runtime rather than shipping a browser engine with the application.

The process-tree RSS values are also not cross-shell equivalent. On macOS, system WebKit processes may not be descendants of the Tauri app process; on Windows, Edge WebView2 processes may be attributable differently. The values remain useful as diagnostics, not as a trustworthy shell ranking.

The shell-ready values are likewise a single cold hosted-runner sample. The direction is notable rather than definitive: Electron reached the shared renderer faster in both measured environments, while the renderer-only CodeMirror initialization result itself varied by platform and engine.

## 4. Hard veto review

### Unsafe file boundary

**No veto observed.** Both implementations passed the bounded lexical and symlink-escape tests. Neither renderer receives unrestricted filesystem access.

### Editor behavior

**No automated veto observed.** Both shells created the same 50,000-word CodeMirror fixture and reached first paint. This is not the professional editor assay from issue #4.

### Accessibility

**Not established. Veto remains live.** Hosted CI did not run VoiceOver, Narrator, NVDA, platform accessibility inspectors, or human keyboard navigation at 200% zoom/high-contrast settings.

### IME and bidi

**Not established. Veto remains live.** The shared renderer carries mixed Japanese/Arabic/Hebrew text, but synthetic insertion is not an IME candidate-window test. Real input methods remain a manual platform control.

### Crash/restart

Both controls implement a crash marker/restart-context mechanism, but the final automated run exercised normal packaged startup rather than deliberately crashing the hosted GUI process. Destructive crash/restart behavior remains an F2 trust drill, not an F1 success claim.

## 5. Decision

**Select Electron 43.2.0 as the F2 desktop shell scaffold.**

This is not a judgement that Electron is universally superior or that Tauri failed. Both survived the automated security/build/runtime controls. The selection is based on the current workbench priorities and the evidence available at this gate:

1. **Renderer consistency matters more than distribution size.** Electron brings one Chromium generation to Windows and macOS. Tauri deliberately delegates to different operating-system WebViews. For a product whose sovereign surface is a high-fidelity professional editor, reducing web-engine variance has unusually high leverage.
2. **The measured shell-ready direction favors Electron.** In this bounded hosted-runner sample, Electron reached the shared renderer materially sooner on both platforms. That result needs real-hardware replication, but it argues against selecting Tauri merely because its package footprint is smaller.
3. **Both can preserve a narrow security boundary.** The Electron control demonstrates that the renderer can remain sandboxed and filesystem-blind while native work stays behind a small explicit bridge. Choosing Electron therefore does not require abandoning file sovereignty or canonical-state rules.
4. **Tauri's strongest measured advantage cannot be over-read.** Its distribution footprint is dramatically smaller, but the collected outputs are not packaging-equivalent and size is explicitly secondary to editor behavior, reliability, and trust.
5. **The native substrate stays separable from the shell.** Vault, mutation, recovery, hashing, compile and catalog contracts should remain behind shell-neutral service interfaces. Selecting Electron must not turn Node/Electron APIs into canonical domain contracts.

## 6. Rejected and retained alternative

Tauri 2 is rejected **as the primary F2 shell scaffold at this gate**, not retired as a fallback. Keep it as the principal shell rival if Electron later triggers a hard veto.

A switch back to Tauri must remain possible without changing project file formats. The shared `ShellBridge` concept demonstrated by this spike should become an explicit implementation boundary.

## 7. Mandatory revisit triggers

Reopen ADR-0004 if any of the following occurs:

- physical Windows/macOS testing reveals a critical Electron IME or accessibility failure;
- issue #4 demonstrates a shell-specific editor-engine behavior that materially favors the OS WebView path;
- F2 real-hardware startup or memory budgets show Electron is materially unacceptable;
- safe Electron implementation requires broad renderer privileges or renderer-owned canonical filesystem mutation;
- platform distribution, signing, update, or native-integration burden becomes materially worse than the Tauri alternative.

## 8. Evidence artifacts

| Control | Artifact | Digest |
|---|---:|---|
| macOS Electron | `9306716059` | `sha256:b107c04a0aa52e0972a9994d56bb8c11997ea9a117340a355637ed325eeadc4b` |
| Windows Electron | `9306721515` | `sha256:11a38af23e55feb52b839561d69b4c1a90dc1ebabf840edae9014696812f9bb3` |
| macOS Tauri | `9306806703` | `sha256:dea93f0b267528091085b4ab12a570625c0e087fb71aa4a1e0861df9c92ca97f` |
| Windows Tauri | `9306895797` | `sha256:81b93a8bf9e6222de29d90f68858da4260d884216021a76a21a6966413dd48cf` |

## 9. F1 route

Issue #3 is closure-ready when this spike PR is reviewed and merged. F1 itself remains `conditional_not_ready`: editor engine #4, compile architecture #5, the issue #7 stacked merge, `CON-003`, adversarial architecture closure, clean promotion validation, and human F1 approval remain independent requirements.
