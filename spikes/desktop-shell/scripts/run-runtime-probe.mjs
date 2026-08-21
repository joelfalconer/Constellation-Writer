import { spawn, execFileSync } from 'node:child_process';
import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const args = Object.fromEntries(process.argv.slice(2).map((arg) => {
  const [k, ...rest] = arg.replace(/^--/, '').split('=');
  return [k, rest.join('=')];
}));
if (!args.binary || !args.report || !args.shell || !args.platform) throw new Error('required: --binary= --report= --shell= --platform=');
const binary = resolve(args.binary);
const report = resolve(args.report);
mkdirSync(dirname(report), { recursive: true });

const child = spawn(binary, [], {
  env: { ...process.env, CW_SPIKE_REPORT: report, CW_SPIKE_AUTO_QUIT_MS: '5000' },
  stdio: ['ignore', 'pipe', 'pipe'],
});
let stdout = '';
let stderr = '';
child.stdout.on('data', (d) => stdout += d.toString());
child.stderr.on('data', (d) => stderr += d.toString());

const deadline = Date.now() + 45000;
while (!existsSync(report) && Date.now() < deadline && child.exitCode === null) {
  await new Promise((r) => setTimeout(r, 200));
}

function processTable() {
  try {
    if (process.platform === 'win32') {
      const script = 'Get-CimInstance Win32_Process | Select-Object ProcessId,ParentProcessId,WorkingSetSize | ConvertTo-Json -Compress';
      const text = execFileSync('powershell', ['-NoProfile', '-Command', script], { encoding: 'utf8' }).trim();
      const value = JSON.parse(text || '[]');
      return (Array.isArray(value) ? value : [value]).map((p) => ({ pid: Number(p.ProcessId), ppid: Number(p.ParentProcessId), rssKb: Number(p.WorkingSetSize || 0) / 1024 }));
    }
    const text = execFileSync('ps', ['-axo', 'pid=,ppid=,rss='], { encoding: 'utf8' });
    return text.trim().split(/\n+/).map((line) => {
      const [pid, ppid, rssKb] = line.trim().split(/\s+/).map(Number);
      return { pid, ppid, rssKb };
    });
  } catch {
    return [];
  }
}

function descendants(table, rootPid) {
  const selected = new Set([rootPid]);
  let changed = true;
  while (changed) {
    changed = false;
    for (const row of table) {
      if (selected.has(row.ppid) && !selected.has(row.pid)) {
        selected.add(row.pid);
        changed = true;
      }
    }
  }
  return table.filter((row) => selected.has(row.pid));
}

let payload = { shell: args.shell, platform: args.platform, runtime_probe: 'failed', child_pid: child.pid, stdout, stderr };
if (existsSync(report)) {
  payload = JSON.parse(readFileSync(report, 'utf8'));
  const rows = descendants(processTable(), child.pid);
  payload.runtime_probe = 'passed';
  payload.process_tree = {
    measured_root_pid: child.pid,
    process_count: rows.length,
    rss_kb: Math.round(rows.reduce((sum, row) => sum + (row.rssKb || 0), 0)),
    note: 'Best-effort process-tree RSS on hosted runner. OS-managed/shared WebView processes may not be attributable to the app process tree.'
  };
  writeFileSync(report, JSON.stringify(payload, null, 2));
}

await new Promise((resolveWait) => {
  if (child.exitCode !== null) return resolveWait();
  const timer = setTimeout(() => { try { child.kill(); } catch {} resolveWait(); }, 8000);
  child.once('exit', () => { clearTimeout(timer); resolveWait(); });
});

if (payload.runtime_probe !== 'passed') {
  console.error(JSON.stringify(payload, null, 2));
  process.exitCode = 2;
} else {
  console.log(JSON.stringify(payload, null, 2));
}
