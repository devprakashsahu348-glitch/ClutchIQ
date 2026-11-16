const bcrypt = require("bcryptjs");
const L = require("../_lib");
const DUMMY = "$2a$12$C6UzMDM.H6dfI/f/IKcEeO7p8n3e2Yp0v9Y9g5qk8wq5Wc1lG0u1e";
module.exports = async (req, res) => {
  if (!L.guard(req, res, "POST")) return;
  try {
    const b = L.body(req), email = L.clean(b.email, 254).toLowerCase(), key = L.ip(req) + "|" + email;
    if (await L.limited("login", key, 5, 15)) return L.send(res, 429, { error: "Too many failed attempts. Try again in 15 minutes." });
    const r = await L.sql`SELECT id,name,email,password_hash FROM users WHERE email=${email}`;
    const u = r[0];
    const ok = await bcrypt.compare(String(b.password || "").slice(0, 72), u ? u.password_hash : DUMMY);
    if (!u || !ok) { await L.record("login", key); return L.send(res, 401, { error: "Incorrect email or password." }); }
    await L.sql`DELETE FROM attempts WHERE kind='login' AND key=${key}`;
    L.setCookie(res, L.sign(u));
    L.send(res, 200, { message: "Logged in." });
  } catch (e) { console.error("login", e.message); L.send(res, 500, { error: "Server error. Please try again." }); }
};
