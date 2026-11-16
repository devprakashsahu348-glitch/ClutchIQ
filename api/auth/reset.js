const bcrypt = require("bcryptjs");
const L = require("../_lib");
module.exports = async (req, res) => {
  if (!L.guard(req, res, "POST")) return;
  try {
    const b = L.body(req), ipa = L.ip(req);
    if (await L.limited("reset", ipa, 10, 60)) return L.send(res, 429, { error: "Too many attempts. Try again later." });
    await L.record("reset", ipa);
    if (!L.pwOk(b.password)) return L.send(res, 400, { error: "Password must be 8-72 characters with upper case, lower case and a number." });
    if (b.password !== b.confirmPassword) return L.send(res, 400, { error: "Passwords do not match." });
    const hash = L.crypto.createHash("sha256").update(String(b.token || "")).digest("hex");
    const r = await L.sql`SELECT id,user_id FROM password_resets WHERE token_hash=${hash} AND used_at IS NULL AND expires_at > now()`;
    if (!r[0]) return L.send(res, 400, { error: "This reset link is invalid or has expired. Please request a new one." });
    const pw = await bcrypt.hash(b.password, 12);
    await L.sql.transaction([
      L.sql`UPDATE users SET password_hash=${pw} WHERE id=${r[0].user_id}`,
      L.sql`UPDATE password_resets SET used_at=now() WHERE user_id=${r[0].user_id} AND used_at IS NULL`,
    ]);
    L.send(res, 200, { message: "Password updated." });
  } catch (e) { console.error("reset", e.message); L.send(res, 500, { error: "Server error. Please try again." }); }
};
