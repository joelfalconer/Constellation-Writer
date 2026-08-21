import { cpSync, existsSync, rmSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const spikeRoot = resolve(here, '..');
const targetName = process.argv[2];
if (targetName !== 'electron') throw new Error('only electron renderer copy is supported');
const source = resolve(spikeRoot, 'shared', 'dist');
const target = resolve(spikeRoot, 'electron', 'renderer');
if (!existsSync(source)) throw new Error(`shared renderer is not built: ${source}`);
rmSync(target, { recursive: true, force: true });
cpSync(source, target, { recursive: true });
console.log(`copied ${source} -> ${target}`);
