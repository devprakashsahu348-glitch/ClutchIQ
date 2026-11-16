const L = require("../_lib");
const GENERIC = { message: "If that email is registered, a reset link is on its way. It works once for 30 minutes." };
module.exports = async (req, res) => {
  if (!L.guard(req, res, "POST")) return;
  try {
    const email = L.clean(L.body(req).email, 254).toLowerCase(), ipa = L.ip(req);
    if (await L.limited("forgot", ipa, 5, 60)) return L.send(res, 429, { error: "Too many requests. Try again later." });
    await L.record("forgot", ipa);
    if (!L.emailOk(email)) return L.send(res, 400, { error: "Please enter a valid email address." });
    const r = await L.sql`SELECT id,name FROM users WHERE email=${email}`;
    if (r[0]) {
      const raw = L.crypto.randomBytes(32).toString("hex"), hash = L.crypto.createHash("sha256").update(raw).digest("hex");
      await L.sql`UPDATE password_resets SET used_at=now() WHERE user_id=${r[0].id} AND used_at IS NULL`;
      await L.sql`INSERT INTO password_resets(user_id,token_hash,expires_at) VALUES(${r[0].id},${hash},now() + interval '30 minutes')`;
      const link = `${L.SITE}/reset?token=${raw}`;
      try {
        await L.mail(email, "Reset your ClutchIQ password", `Hi ${r[0].name},\n\nUse this link to set a new password. It works once and expires in 30 minutes:\n${link}\n\nIf you did not ask for this, ignore this email.\n\nClutchIQ`,
          `<p>Hi ${r[0].name.replace(/</g, "&lt;")},</p><p><a href="${link}">Set a new password</a>. The link works once and expires in 30 minutes.</p><p>If you did not ask for this, ignore this email.</p>`);
      } catch (e) { console.error("mail", e.message); }
    }
    L.send(res, 200, GENERIC);
  } catch (e) { console.error("forgot", e.message); L.send(res, 500, { error: "Server error. Please try again." }); }
};
