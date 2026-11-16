const L = require("./_lib");
module.exports = async (req, res) => {
  if (!L.guard(req, res, "POST")) return;
  try {
    const b = L.body(req), name = L.clean(b.name, 80), email = L.clean(b.email, 254), msg = L.clean(b.message, 2000), ipa = L.ip(req);
    if (await L.limited("contact", ipa, 5, 60)) return L.send(res, 429, { error: "Too many messages. Try again later." });
    if (name.length < 2 || !L.emailOk(email) || msg.length < 10) return L.send(res, 400, { error: "Please fill in your name, a valid email and a message of at least 10 characters." });
    await L.record("contact", ipa);
    await L.sql`INSERT INTO contacts(name,email,message) VALUES(${name},${email},${msg})`;
    try { await L.mail(process.env.CONTACT_TO || process.env.SMTP_USER, `ClutchIQ contact: ${name}`, `${name} <${email}>\n\n${msg}`, undefined, email); } catch (e) { console.error("mail", e.message); }
    L.send(res, 200, { message: "Thanks! Your message has been sent. We will reply soon." });
  } catch (e) { console.error("contact", e.message); L.send(res, 500, { error: "Server error. Please try again." }); }
};
