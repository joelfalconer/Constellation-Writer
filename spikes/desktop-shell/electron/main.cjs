const { app, BrowserWindow, Menu, dialog, ipcMain, clipboard } = require('electron');
const fs = require('node:fs');
const path = require('node:path');
const { performance } = require('node:perf_hooks');
const { resolveInsideProject } = require('./path-boundary.cjs');

const startupAt = performance.now();
let mainWindow = null;
let projectRoot = null;
let watcher = null;
const restartMarker = path.join(app.getPath('temp'), 'cw-electron-shell-spike-restart.json');

function rendererPath() {
  return path.join(__dirname, 'renderer', 'index.html');
}

function send(channel, payload) {
  if (mainWindow && !mainWindow.isDestroyed()) mainWindow.webContents.send(channel, payload);
}

function installMenu() {
  const menu = Menu.buildFromTemplate([
    {
      label: 'Spike',
      submenu: [
        {
          label: 'Spike Command',
          accelerator: 'CmdOrCtrl+Shift+P',
          click: () => send('menu-command', 'spike-command'),
        },
      ],
    },
  ]);
  Menu.setApplicationMenu(menu);
}

async function atomicWrite(relativePath, content) {
  const target = resolveInsideProject(projectRoot, relativePath);
  const temp = `${target}.cwtmp-${process.pid}-${Date.now()}`;
  const handle = await fs.promises.open(temp, 'wx', 0o600);
  try {
    await handle.writeFile(content, 'utf8');
    await handle.sync();
  } finally {
    await handle.close();
  }
  await fs.promises.rename(temp, target);
  try {
    const dirHandle = await fs.promises.open(path.dirname(target), 'r');
    try { await dirHandle.sync(); } finally { await dirHandle.close(); }
  } catch { /* directory fsync is platform-dependent */ }
  return { ok: true, target };
}

function startWatcher() {
  if (!projectRoot) throw new Error('project root is not selected');
  watcher?.close();
  watcher = fs.watch(projectRoot, { recursive: true }, (eventType, filename) => {
    send('file-watch', { eventType, filename: filename?.toString() ?? null });
  });
  return { ok: true, root: projectRoot };
}

ipcMain.handle('open-project', async () => {
  const result = await dialog.showOpenDialog(mainWindow, { properties: ['openDirectory'] });
  if (result.canceled || !result.filePaths[0]) return null;
  projectRoot = fs.realpathSync(result.filePaths[0]);
  return projectRoot;
});
ipcMain.handle('save-as', async () => {
  const result = await dialog.showSaveDialog(mainWindow, { title: 'Shell spike save dialog' });
  return result.canceled ? null : result.filePath ?? null;
});
ipcMain.handle('start-watch', () => startWatcher());
ipcMain.handle('atomic-write', (_event, { relativePath, content }) => atomicWrite(relativePath, content));
ipcMain.handle('read-clipboard', () => clipboard.readText());
ipcMain.handle('write-clipboard', (_event, text) => { clipboard.writeText(String(text)); return { ok: true }; });
ipcMain.handle('restart-context', () => {
  if (!fs.existsSync(restartMarker)) return null;
  const text = fs.readFileSync(restartMarker, 'utf8');
  fs.unlinkSync(restartMarker);
  return JSON.parse(text);
});
ipcMain.handle('crash-fixture', () => {
  fs.writeFileSync(restartMarker, JSON.stringify({ crashed_at: new Date().toISOString(), shell: 'electron' }));
  process.crash();
});
ipcMain.on('native-drop-captured', (_event, paths) => send('native-drop', paths));
ipcMain.handle('spike-ready', async (_event, metrics) => {
  const memory = await process.getProcessMemoryInfo();
  const report = {
    shell: 'electron',
    pid: process.pid,
    startup_to_renderer_ready_ms: Number((performance.now() - startupAt).toFixed(3)),
    main_process_memory_kb: memory,
    renderer: metrics,
  };
  const reportPath = process.env.CW_SPIKE_REPORT;
  if (reportPath) fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
  if (process.env.CW_SPIKE_AUTO_QUIT_MS) setTimeout(() => app.quit(), Number(process.env.CW_SPIKE_AUTO_QUIT_MS));
  return report;
});

app.whenReady().then(() => {
  installMenu();
  mainWindow = new BrowserWindow({
    width: 1100,
    height: 760,
    show: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      webSecurity: true,
    },
  });
  mainWindow.webContents.setWindowOpenHandler(() => ({ action: 'deny' }));
  mainWindow.webContents.on('will-navigate', (event, url) => {
    if (!url.startsWith('file:')) event.preventDefault();
  });
  mainWindow.loadFile(rendererPath());
});

app.on('window-all-closed', () => app.quit());
