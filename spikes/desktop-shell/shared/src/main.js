import { basicSetup, EditorView } from 'codemirror';
import { EditorState } from '@codemirror/state';
import { markdown } from '@codemirror/lang-markdown';
import { getShellBridge } from './bridge.js';
import './styles.css';

const bridge = getShellBridge();
const status = document.querySelector('#status-text');
const rootLabel = document.querySelector('#project-root');
document.querySelector('#shell-name').textContent = bridge.name;

const sentence = 'Local first writing keeps durable work legible calm recoverable portable.';
const fixture = Array.from({ length: 5000 }, () => sentence).join('\n');
const expectedWords = 50000;
const actualWords = fixture.trim().split(/\s+/u).length;
if (actualWords !== expectedWords) throw new Error(`fixture word count ${actualWords} != ${expectedWords}`);

const initStart = performance.now();
const state = EditorState.create({
  doc: fixture,
  extensions: [
    basicSetup,
    markdown(),
    EditorView.lineWrapping,
    EditorView.contentAttributes.of({
      'aria-label': '50,000-word CodeMirror editor placeholder',
      'data-spike-fixture': '50k',
    }),
  ],
});
const view = new EditorView({ state, parent: document.querySelector('#editor') });
const editorInitMs = performance.now() - initStart;

const mixedScript = '日本語入力 العربية المختلطة עברית mixed-script';
view.dispatch({ changes: { from: 0, insert: `${mixedScript}\n\n` } });
view.dispatch({ changes: { from: 0, to: mixedScript.length + 2, insert: '' } });

let projectRoot = null;

function setStatus(text) {
  status.textContent = text;
}

async function safeCall(label, fn) {
  try {
    const result = await fn();
    setStatus(`${label}: ${typeof result === 'string' ? result : JSON.stringify(result)}`);
    return result;
  } catch (error) {
    setStatus(`${label} failed: ${error?.message ?? error}`);
    return null;
  }
}

document.querySelector('#open-project').addEventListener('click', async () => {
  const selected = await safeCall('project', () => bridge.openProject());
  if (selected) {
    projectRoot = selected;
    rootLabel.textContent = selected;
  }
});

document.querySelector('#save-as').addEventListener('click', () => safeCall('save dialog', () => bridge.saveAs()));
document.querySelector('#start-watch').addEventListener('click', () => safeCall('watch', () => bridge.startWatch()));
document.querySelector('#atomic-write').addEventListener('click', () => safeCall('atomic write', () => bridge.atomicWrite('.cw-shell-spike.txt', `probe ${new Date().toISOString()}\n`)));
document.querySelector('#copy').addEventListener('click', () => safeCall('clipboard write', () => bridge.writeClipboard('Constellation Writer shell spike')));
document.querySelector('#paste').addEventListener('click', () => safeCall('clipboard read', () => bridge.readClipboard()));
document.querySelector('#crash').addEventListener('click', () => bridge.crashFixture());

const dropZone = document.querySelector('#drop-zone');
dropZone.addEventListener('dragover', (event) => {
  event.preventDefault();
  dropZone.classList.add('over');
});
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('over'));
dropZone.addEventListener('drop', (event) => {
  event.preventDefault();
  dropZone.classList.remove('over');
  const names = [...event.dataTransfer.files].map((file) => file.name);
  setStatus(`DOM drop: ${names.join(', ') || 'no files'}`);
});

await bridge.onMenuCommand?.((command) => setStatus(`native menu: ${command}`));
await bridge.onWatch?.((event) => setStatus(`watch event: ${JSON.stringify(event)}`));
await bridge.onNativeDrop?.((paths) => setStatus(`native drop: ${JSON.stringify(paths)}`));

const restart = await safeCall('restart context', () => bridge.restartContext());

requestAnimationFrame(() => {
  requestAnimationFrame(async () => {
    const firstPaintMs = performance.now() - initStart;
    const metrics = {
      shell: bridge.name,
      fixture_words: expectedWords,
      editor_init_ms: Number(editorInitMs.toFixed(3)),
      first_paint_ms: Number(firstPaintMs.toFixed(3)),
      user_agent: navigator.userAgent,
      platform: navigator.platform,
      restart_context_present: Boolean(restart),
      project_root_selected: Boolean(projectRoot),
    };
    setStatus(`ready: ${JSON.stringify(metrics)}`);
    await bridge.readyProbe(metrics);
  });
});
