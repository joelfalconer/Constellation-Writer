function electronBridge() {
  const api = window.cwShell;
  return {
    name: 'electron',
    openProject: () => api.openProject(),
    saveAs: () => api.saveAs(),
    startWatch: () => api.startWatch(),
    atomicWrite: (relativePath, content) => api.atomicWrite(relativePath, content),
    readClipboard: () => api.readClipboard(),
    writeClipboard: (text) => api.writeClipboard(text),
    crashFixture: () => api.crashFixture(),
    restartContext: () => api.restartContext(),
    readyProbe: (metrics) => api.readyProbe(metrics),
    onMenuCommand: (handler) => api.onMenuCommand(handler),
    onWatch: (handler) => api.onWatch(handler),
    onNativeDrop: (handler) => api.onNativeDrop(handler),
  };
}

function tauriBridge() {
  const invoke = (command, args = {}) => window.__TAURI__.core.invoke(command, args);
  return {
    name: 'tauri',
    openProject: () => invoke('select_project_root'),
    saveAs: () => invoke('save_as_dialog'),
    startWatch: () => invoke('start_watch'),
    atomicWrite: (relativePath, content) => invoke('atomic_write_placeholder', { relativePath, content }),
    readClipboard: () => invoke('read_clipboard'),
    writeClipboard: (text) => invoke('write_clipboard', { text }),
    crashFixture: () => invoke('crash_fixture'),
    restartContext: () => invoke('restart_context'),
    readyProbe: (metrics) => invoke('spike_ready', { metrics }),
    onMenuCommand: async (handler) => window.__TAURI__.event.listen('menu-command', (event) => handler(event.payload)),
    onWatch: async (handler) => window.__TAURI__.event.listen('file-watch', (event) => handler(event.payload)),
    onNativeDrop: async (handler) => {
      const webview = window.__TAURI__.webview.getCurrentWebview();
      return webview.onDragDropEvent((event) => {
        if (event.payload.type === 'drop') handler(event.payload.paths);
      });
    },
  };
}

function browserFallback() {
  return {
    name: 'browser-fallback',
    openProject: async () => null,
    saveAs: async () => null,
    startWatch: async () => ({ unsupported: true }),
    atomicWrite: async () => ({ unsupported: true }),
    readClipboard: async () => navigator.clipboard?.readText?.() ?? '',
    writeClipboard: async (text) => navigator.clipboard?.writeText?.(text),
    crashFixture: async () => ({ unsupported: true }),
    restartContext: async () => null,
    readyProbe: async () => null,
    onMenuCommand: async () => null,
    onWatch: async () => null,
    onNativeDrop: async () => null,
  };
}

export function getShellBridge() {
  if (window.cwShell) return electronBridge();
  if (window.__TAURI__?.core?.invoke) return tauriBridge();
  return browserFallback();
}
