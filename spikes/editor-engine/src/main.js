import "./styles.css";
import { mountCodeMirror } from "./codemirror.js";
import { mountProseMirror } from "./prosemirror.js";

const params = new URLSearchParams(window.location.search);
const engine = params.get("engine") === "prosemirror" ? "prosemirror" : "codemirror6";
const host = document.querySelector("#editor-host");
const status = document.querySelector("#status");

const api = engine === "prosemirror" ? mountProseMirror(host) : mountCodeMirror(host);
window.editorSpike = api;
status.textContent = `${api.engine} ready`;

document.querySelector("#draft-mode").addEventListener("click", () => api.setMode("draft"));
document.querySelector("#revise-mode").addEventListener("click", () => api.setMode("revise"));
document.querySelector("#toggle-pane").addEventListener("click", () => api.togglePane());
let typewriter = false;
document.querySelector("#toggle-typewriter").addEventListener("click", () => {
  typewriter = !typewriter;
  api.setTypewriter(typewriter);
});
