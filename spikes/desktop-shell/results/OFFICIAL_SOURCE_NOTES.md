# Official Technical Source Notes

Access date: 2026-08-18

## Tauri 2

- Tauri ecosystem releases list core `tauri` 2.11.5 and CLI 2.11.4 in the current official release registry.
- Windows uses Microsoft Edge WebView2; macOS development relies on Xcode tooling and the platform WebKit stack.
- Tauri Runtime Authority checks capabilities, permissions, origins, and scopes before commands are invoked.
- Command/plugin scopes are granular but command authors remain responsible for preventing scope bypasses.
- The filesystem plugin documents traversal protection, symlink-sensitive stat behavior, scoped permissions, and native watch support.
- Native window menus, dialog, clipboard, and global-shortcut facilities are available through core/plugins.
- Tauri bundles through its CLI and uses platform code signing/notarization for distribution.

Primary sources:
- https://v2.tauri.app/release/
- https://v2.tauri.app/start/prerequisites/
- https://v2.tauri.app/security/runtime-authority/
- https://v2.tauri.app/security/scope/
- https://v2.tauri.app/plugin/file-system/
- https://v2.tauri.app/plugin/clipboard/
- https://v2.tauri.app/plugin/dialog/
- https://v2.tauri.app/learn/window-menu/
- https://v2.tauri.app/distribute/

## Electron

- Electron 43.2.0 is the current stable 43.x release in the official release registry used for this spike and bundles Chromium 150 with Node 24.18.0.
- Electron recommends context isolation, renderer sandboxing, no Node integration for renderer content, restrictive navigation, validated IPC senders, and a restrictive CSP.
- Context isolation is default from Electron 12 and renderer sandboxing is default from Electron 20, but the application must still expose only narrow validated APIs.
- Electron packages the Electron/Chromium runtime with the application. Electron Forge is the recommended official distribution toolkit, with platform signing/notarization required for trusted distribution.

Primary sources:
- https://releases.electronjs.org/release/v43.2.0
- https://www.electronjs.org/docs/latest/tutorial/security
- https://www.electronjs.org/docs/latest/tutorial/context-isolation
- https://www.electronjs.org/docs/latest/tutorial/sandbox
- https://www.electronjs.org/docs/latest/tutorial/distribution-overview
- https://www.electronjs.org/docs/latest/tutorial/code-signing

## Epistemic boundary

Documentation establishes supported mechanisms and recommended security posture. It does not establish Constellation Writer's actual latency, accessibility quality, IME fidelity, recovery behavior, or user preference. Those require the executable spike and later human assays.
