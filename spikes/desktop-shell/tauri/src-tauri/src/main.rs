#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use notify::{Config, RecommendedWatcher, RecursiveMode, Watcher};
use serde_json::{json, Value};
use std::{
    fs::{self, OpenOptions},
    io::Write,
    path::{Component, Path, PathBuf},
    sync::Mutex,
    time::{Duration, Instant},
};
use tauri::{menu::{MenuBuilder, MenuItemBuilder}, AppHandle, Emitter, Manager, State};
use tauri_plugin_clipboard_manager::ClipboardExt;
use tauri_plugin_dialog::DialogExt;

struct ShellState {
    project_root: Mutex<Option<PathBuf>>,
    watcher: Mutex<Option<RecommendedWatcher>>,
    startup: Instant,
    restart_marker: PathBuf,
}

fn within(root: &Path, candidate: &Path) -> bool {
    candidate == root || candidate.starts_with(root)
}

fn resolve_inside_project(root: &Path, relative: &str) -> Result<PathBuf, String> {
    let rel = Path::new(relative);
    if rel.is_absolute() || rel.components().any(|c| matches!(c, Component::ParentDir | Component::RootDir | Component::Prefix(_))) {
        return Err("path escapes project root".into());
    }
    let canonical_root = fs::canonicalize(root).map_err(|e| e.to_string())?;
    let candidate = canonical_root.join(rel);
    let parent = candidate.parent().ok_or("target has no parent")?;
    let canonical_parent = fs::canonicalize(parent).map_err(|e| e.to_string())?;
    if !within(&canonical_root, &canonical_parent) {
        return Err("symlink parent escapes project root".into());
    }
    if candidate.exists() {
        let canonical_target = fs::canonicalize(&candidate).map_err(|e| e.to_string())?;
        if !within(&canonical_root, &canonical_target) {
            return Err("symlink target escapes project root".into());
        }
    }
    Ok(candidate)
}

#[tauri::command]
async fn select_project_root(app: AppHandle, state: State<'_, ShellState>) -> Result<Option<String>, String> {
    let selected = app.dialog().file().blocking_pick_folder();
    let Some(file_path) = selected else { return Ok(None) };
    let path = file_path.into_path().map_err(|_| "selected location is not a filesystem path".to_string())?;
    let canonical = fs::canonicalize(path).map_err(|e| e.to_string())?;
    *state.project_root.lock().map_err(|_| "project-root lock poisoned")? = Some(canonical.clone());
    Ok(Some(canonical.to_string_lossy().into_owned()))
}

#[tauri::command]
async fn save_as_dialog(app: AppHandle) -> Result<Option<String>, String> {
    let selected = app.dialog().file().blocking_save_file();
    let Some(file_path) = selected else { return Ok(None) };
    let path = file_path.into_path().map_err(|_| "selected location is not a filesystem path".to_string())?;
    Ok(Some(path.to_string_lossy().into_owned()))
}

#[tauri::command]
fn write_clipboard(app: AppHandle, text: String) -> Result<Value, String> {
    app.clipboard().write_text(text).map_err(|e| e.to_string())?;
    Ok(json!({"ok": true}))
}

#[tauri::command]
fn read_clipboard(app: AppHandle) -> Result<String, String> {
    app.clipboard().read_text().map_err(|e| e.to_string())
}

#[tauri::command]
fn start_watch(app: AppHandle, state: State<'_, ShellState>) -> Result<Value, String> {
    let root = state.project_root.lock().map_err(|_| "project-root lock poisoned")?.clone().ok_or("project root is not selected")?;
    let app_for_events = app.clone();
    let mut watcher = RecommendedWatcher::new(
        move |result: notify::Result<notify::Event>| {
            if let Ok(event) = result {
                let payload = json!({
                    "kind": format!("{:?}", event.kind),
                    "paths": event.paths.iter().map(|p| p.to_string_lossy().into_owned()).collect::<Vec<_>>()
                });
                let _ = app_for_events.emit("file-watch", payload);
            }
        },
        Config::default(),
    ).map_err(|e| e.to_string())?;
    watcher.watch(&root, RecursiveMode::Recursive).map_err(|e| e.to_string())?;
    *state.watcher.lock().map_err(|_| "watcher lock poisoned")? = Some(watcher);
    Ok(json!({"ok": true, "root": root.to_string_lossy()}))
}

#[tauri::command]
fn atomic_write_placeholder(state: State<'_, ShellState>, relative_path: String, content: String) -> Result<Value, String> {
    let root = state.project_root.lock().map_err(|_| "project-root lock poisoned")?.clone().ok_or("project root is not selected")?;
    let target = resolve_inside_project(&root, &relative_path)?;
    let temp = target.with_extension(format!("cwtmp-{}-{}", std::process::id(), state.startup.elapsed().as_nanos()));
    let mut file = OpenOptions::new().write(true).create_new(true).open(&temp).map_err(|e| e.to_string())?;
    file.write_all(content.as_bytes()).map_err(|e| e.to_string())?;
    file.sync_all().map_err(|e| e.to_string())?;
    drop(file);
    fs::rename(&temp, &target).map_err(|e| e.to_string())?;
    if let Ok(dir) = OpenOptions::new().read(true).open(target.parent().unwrap_or(&root)) {
        let _ = dir.sync_all();
    }
    Ok(json!({"ok": true, "target": target.to_string_lossy()}))
}

#[tauri::command]
fn restart_context(state: State<'_, ShellState>) -> Result<Option<Value>, String> {
    if !state.restart_marker.exists() { return Ok(None) }
    let text = fs::read_to_string(&state.restart_marker).map_err(|e| e.to_string())?;
    let _ = fs::remove_file(&state.restart_marker);
    serde_json::from_str(&text).map(Some).map_err(|e| e.to_string())
}

#[tauri::command]
fn crash_fixture(state: State<'_, ShellState>) -> Result<(), String> {
    fs::write(&state.restart_marker, json!({"shell":"tauri","crashed_at":"fixture"}).to_string()).map_err(|e| e.to_string())?;
    std::process::abort();
}

#[tauri::command]
fn spike_ready(app: AppHandle, state: State<'_, ShellState>, metrics: Value) -> Result<Value, String> {
    let report = json!({
        "shell": "tauri",
        "pid": std::process::id(),
        "startup_to_renderer_ready_ms": state.startup.elapsed().as_secs_f64() * 1000.0,
        "renderer": metrics
    });
    if let Ok(path) = std::env::var("CW_SPIKE_REPORT") {
        fs::write(path, serde_json::to_vec_pretty(&report).map_err(|e| e.to_string())?).map_err(|e| e.to_string())?;
    }
    if let Ok(delay) = std::env::var("CW_SPIKE_AUTO_QUIT_MS") {
        if let Ok(ms) = delay.parse::<u64>() {
            let handle = app.clone();
            std::thread::spawn(move || {
                std::thread::sleep(Duration::from_millis(ms));
                handle.exit(0);
            });
        }
    }
    Ok(report)
}

fn main() {
    let startup = Instant::now();
    let restart_marker = std::env::temp_dir().join("cw-tauri-shell-spike-restart.json");
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_clipboard_manager::init())
        .manage(ShellState { project_root: Mutex::new(None), watcher: Mutex::new(None), startup, restart_marker })
        .invoke_handler(tauri::generate_handler![select_project_root, save_as_dialog, write_clipboard, read_clipboard, start_watch, atomic_write_placeholder, restart_context, crash_fixture, spike_ready])
        .setup(|app| {
            let command = MenuItemBuilder::with_id("spike-command", "Spike Command")
                .accelerator("CmdOrCtrl+Shift+P")
                .build(app)?;
            let menu = MenuBuilder::new(app).item(&command).build()?;
            app.set_menu(menu)?;
            app.on_menu_event(|app_handle, event| {
                if event.id().0.as_str() == "spike-command" {
                    let _ = app_handle.emit("menu-command", "spike-command");
                }
            });
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running Tauri shell spike");
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;

    #[test]
    fn allows_child_path() {
        let dir = tempdir().unwrap();
        let root = dir.path().join("project");
        fs::create_dir(&root).unwrap();
        let resolved = resolve_inside_project(&root, "sheet.md").unwrap();
        assert_eq!(resolved, fs::canonicalize(&root).unwrap().join("sheet.md"));
    }

    #[test]
    fn rejects_parent_escape() {
        let dir = tempdir().unwrap();
        let root = dir.path().join("project");
        fs::create_dir(&root).unwrap();
        assert!(resolve_inside_project(&root, "../escape.md").is_err());
    }

    #[cfg(unix)]
    #[test]
    fn rejects_symlink_parent_escape() {
        use std::os::unix::fs::symlink;
        let dir = tempdir().unwrap();
        let root = dir.path().join("project");
        let outside = dir.path().join("outside");
        fs::create_dir(&root).unwrap();
        fs::create_dir(&outside).unwrap();
        symlink(&outside, root.join("link")).unwrap();
        assert!(resolve_inside_project(&root, "link/escape.md").is_err());
    }
}
