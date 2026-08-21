const fs = require('node:fs');
const path = require('node:path');

function within(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative === '' || (!relative.startsWith(`..${path.sep}`) && relative !== '..' && !path.isAbsolute(relative));
}

function resolveInsideProject(projectRoot, relativePath) {
  if (!projectRoot) throw new Error('project root is not selected');
  if (path.isAbsolute(relativePath)) throw new Error('absolute paths are not allowed');
  const root = fs.realpathSync(projectRoot);
  const candidate = path.resolve(root, relativePath);
  if (!within(root, candidate)) throw new Error('path escapes project root');
  const parent = path.dirname(candidate);
  const realParent = fs.realpathSync(parent);
  if (!within(root, realParent)) throw new Error('symlink parent escapes project root');
  if (fs.existsSync(candidate)) {
    const realTarget = fs.realpathSync(candidate);
    if (!within(root, realTarget)) throw new Error('symlink target escapes project root');
  }
  return candidate;
}

module.exports = { resolveInsideProject, within };
