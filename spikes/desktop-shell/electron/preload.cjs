const { contextBridge, ipcRenderer, webUtils } = require('electron');

contextBridge.exposeInMainWorld('cwShell', {
  openProject: () => ipcRenderer.invoke('open-project'),
  saveAs: () => ipcRenderer.invoke('save-as'),
  startWatch: () => ipcRenderer.invoke('start-watch'),
  atomicWrite: (relativePath, content) => ipcRenderer.invoke('atomic-write', { relativePath, content }),
  readClipboard: () => ipcRenderer.invoke('read-clipboard'),
  writeClipboard: (text) => ipcRenderer.invoke('write-clipboard', text),
  crashFixture: () => ipcRenderer.invoke('crash-fixture'),
  restartContext: () => ipcRenderer.invoke('restart-context'),
  readyProbe: (metrics) => ipcRenderer.invoke('spike-ready', metrics),
  onMenuCommand: (callback) => ipcRenderer.on('menu-command', (_event, payload) => callback(payload)),
  onWatch: (callback) => ipcRenderer.on('file-watch', (_event, payload) => callback(payload)),
  onNativeDrop: (callback) => ipcRenderer.on('native-drop', (_event, payload) => callback(payload)),
});

window.addEventListener('DOMContentLoaded', () => {
  document.addEventListener('dragover', (event) => event.preventDefault());
  document.addEventListener('drop', (event) => {
    event.preventDefault();
    const paths = [];
    for (const file of event.dataTransfer?.files ?? []) {
      try { paths.push(webUtils.getPathForFile(file)); } catch { /* preserve DOM fallback */ }
    }
    ipcRenderer.send('native-drop-captured', paths.filter(Boolean));
  });
});
