const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { resolveInsideProject } = require('../path-boundary.cjs');

function fixture() {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), 'cw-shell-boundary-'));
  const root = path.join(base, 'project');
  const outside = path.join(base, 'outside');
  fs.mkdirSync(root);
  fs.mkdirSync(outside);
  return { base, root, outside };
}

test('allows a path whose parent resolves inside project root', () => {
  const { base, root } = fixture();
  try {
    assert.equal(resolveInsideProject(root, 'sheet.md'), path.join(fs.realpathSync(root), 'sheet.md'));
  } finally { fs.rmSync(base, { recursive: true, force: true }); }
});

test('rejects lexical parent traversal', () => {
  const { base, root } = fixture();
  try {
    assert.throws(() => resolveInsideProject(root, '../escape.md'), /escapes project root/);
  } finally { fs.rmSync(base, { recursive: true, force: true }); }
});

test('rejects a symlinked parent that escapes project root', (t) => {
  const { base, root, outside } = fixture();
  const link = path.join(root, 'link');
  try {
    try {
      fs.symlinkSync(outside, link, process.platform === 'win32' ? 'junction' : 'dir');
    } catch (error) {
      t.skip(`symlink fixture unavailable: ${error.code ?? error.message}`);
      return;
    }
    assert.throws(() => resolveInsideProject(root, 'link/escape.md'), /symlink parent escapes project root/);
  } finally { fs.rmSync(base, { recursive: true, force: true }); }
});
