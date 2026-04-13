export function $(sel, root = document) {
  return root.querySelector(sel);
}
export function $all(sel, root = document) {
  return Array.from(root.querySelectorAll(sel));
}

export function setText(el, text) {
  if (!el) return;
  el.textContent = text ?? "";
}

export function escapeHtml(s) {
  return String(s ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

export function readSession() {
  const raw = sessionStorage.getItem("courseduck.session");
  if (!raw) return null;
  try { return JSON.parse(raw); } catch { return null; }
}

export function writeSession(session) {
  sessionStorage.setItem("courseduck.session", JSON.stringify(session));
}

export function clearSession() {
  sessionStorage.removeItem("courseduck.session");
}

export function readProfile() {
  const raw = localStorage.getItem("courseduck.profile");
  if (!raw) return null;
  try { return JSON.parse(raw); } catch { return null; }
}

export function writeProfile(profile) {
  localStorage.setItem("courseduck.profile", JSON.stringify(profile));
}

export function toast({ title, message, actions = [] }) {
  const box = document.createElement("div");
  box.className = "toast show";
  box.innerHTML = `
    <div class="title"></div>
    <div class="msg"></div>
    <div class="actions"></div>
  `;
  setText(box.querySelector(".title"), title || "提示");
  setText(box.querySelector(".msg"), message || "");
  const actionsEl = box.querySelector(".actions");
  actions.forEach((a) => {
    const b = document.createElement("button");
    b.className = `btn ${a.variant || ""}`.trim();
    b.type = "button";
    b.textContent = a.label || "确定";
    b.addEventListener("click", () => {
      try { a.onClick && a.onClick(); } finally { box.remove(); }
    });
    actionsEl.appendChild(b);
  });
  if (actions.length === 0) {
    const b = document.createElement("button");
    b.className = "btn";
    b.type = "button";
    b.textContent = "知道了";
    b.addEventListener("click", () => box.remove());
    actionsEl.appendChild(b);
  }
  document.body.appendChild(box);
  setTimeout(() => {
    if (document.body.contains(box)) box.remove();
  }, 5200);
}

export function requireLogin({ redirectTo = "login.html" } = {}) {
  const s = readSession();
  if (!s?.token) {
    window.location.href = redirectTo;
    return null;
  }
  return s;
}

