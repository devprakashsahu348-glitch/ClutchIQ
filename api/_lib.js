const { neon } = require("@neondatabase/serverless");
const jwt = require("jsonwebtoken");
const crypto = require("crypto");
const nodemailer = require("nodemailer");
const sql = neon(process.env.DATABASE_URL);
const SITE = (process.env.SITE_URL || "").replace(/\/$/, "");
const COOKIE = "session";
const send = (res, code, obj) => { res.statusCode = code; res.setHeader("Content-Type", "application/json"); res.setHeader("Cache-Control", "no-store"); res.end(JSON.stringify(obj)); };
const ip = (req) => (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "unknown";
function guard(req, res, method) {
  if (req.method !== method) { send(res, 405, { error: "Method not allowed." }); return false; }
  if (method === "POST") {
    const o = req.headers.origin;
    if (o && SITE && o.replace(/\/$/, "") !== SITE && !/^https:\/\/[\w-]+\.vercel\.app$/.test(o)) { send(res, 403, { error: "Forbidden." }); return false; }
    if (!(req.headers["content-type"] || "").includes("application/json")) { send(res, 415, { error: "Unsupported request." }); return false; }
  }
  return true;
}
const body = (req) => (typeof req.body === "string" ? JSON.parse(req.body || "{}") : req.body || {});
const clean = (s, n) => String(s || "").trim().slice(0, n);
const emailOk = (e) => /^[^\s@]{1,64}@[^\s@]+\.[^\s@]{2,}$/.test(e) && e.length <= 254;
const pwOk = (p) => typeof p === "string" && p.length >= 8 && p.length <= 72 && /[a-z]/.test(p) && /[A-Z]/.test(p) && /\d/.test(p);
async function limited(kind, key, max, minutes) {
  const r = await sql`SELECT count(*)::int AS n FROM attempts WHERE kind=${kind} AND key=${key} AND created_at > now() - make_interval(mins => ${minutes})`;
  return r[0].n >= max;
}
const record = (kind, key) => sql`INSERT INTO attempts(kind,key) VALUES(${kind},${key})`;
const sign = (u) => jwt.sign({ uid: u.id }, process.env.JWT_SECRET, { expiresIn: "7d" });
const setCookie = (res, t) => res.setHeader("Set-Cookie", `${COOKIE}=${t}; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=604800`);
const clearCookie = (res) => res.setHeader("Set-Cookie", `${COOKIE}=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0`);
async function currentUser(req) {
  const m = (req.headers.cookie || "").match(/(?:^|;\s*)session=([^;]+)/);
  if (!m) return null;
  try {
    const { uid } = jwt.verify(m[1], process.env.JWT_SECRET);
    const r = await sql`SELECT id,name,email FROM users WHERE id=${uid}`;
    return r[0] || null;
  } catch { return null; }
}
async function mail(to, subject, text, html, replyTo) {
  if (!process.env.SMTP_USER || !process.env.SMTP_PASS) throw new Error("SMTP not configured");
  const t = nodemailer.createTransport({ host: process.env.SMTP_HOST || "smtp.gmail.com", port: 465, secure: true, auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS } });
  await t.sendMail({ from: `"ClutchIQ" <${process.env.SMTP_USER}>`, to, subject, text, html, replyTo });
}
module.exports = { sql, crypto, send, ip, guard, body, clean, emailOk, pwOk, limited, record, sign, setCookie, clearCookie, currentUser, mail, SITE };
