const bcrypt = require("bcryptjs");
const L = require("../_lib");
module.exports = async (req, res) => {
  if (!L.guard(req, res, "POST")) return;
  try {
    const b = L.body(req), name = L.clean(b.name, 80), email = L.clean(b.email, 254).toLowerCase(), ipa = L.ip(req);
    if (await L.limited("signup", ipa, 10, 60)) return L.send(res, 429, { error: "Too many sign-up attempts. Try again later." });
    await L.record("signup", ipa);
    if (name.length < 2) return L.send(res, 400, { error: "Please enter your full name." });
    if (!L.emailOk(email)) return L.send(res, 400, { error: "Please enter a valid email address." });
    if (!L.pwOk(b.password)) return L.send(res, 400, { error: "Password must be 8-72 characters with upper case, lower case and a number." });
    if (b.password !== b.confirmPassword) return L.send(res, 400, { error: "Passwords do not match." });
    if (!b.agree) return L.send(res, 400, { error: "Please accept the Terms and Privacy policy." });
    const hash = await bcrypt.hash(b.password, 12);
    const utm = b.utm && typeof b.utm === "object" ? JSON.stringify(b.utm).slice(0, 600) : null;
    try {
      await L.sql`INSERT INTO users(name,email,password_hash,utm) VALUES(${name},${email},${hash},${utm})`;
    } catch (e) {
      if (e.code === "23505") return L.send(res, 409, { error: "An account with this email already exists. Try logging in." });
      throw e;
    }
    L.send(res, 201, { message: "Account created." });
  } catch (e) { console.error("signup", e.message); L.send(res, 500, { error: "Server error. Please try again." }); }
};
