"""Generates the static site into /public. Usage: python build.py https://your-domain.com [GA_ID] [WHATSAPP_NUMBER_DIGITS]"""
import sys, json, datetime, pathlib
SITE = (sys.argv[1] if len(sys.argv) > 1 else "https://clutchiq.vercel.app").rstrip("/")
GA = sys.argv[2] if len(sys.argv) > 2 else ""
WA = sys.argv[3] if len(sys.argv) > 3 else ""
EMAIL, OWNER, NAME = "devprakashsahu348@gmail.com", "Dev Prakash Sahu", "ClutchIQ"
TODAY = datetime.date.today(); UPD = TODAY.strftime("%d %B %Y"); ISO = TODAY.isoformat()
R = json.load(open("data/rankings.json")); M = R["meta"]
P = pathlib.Path("public"); (P / "assets").mkdir(parents=True, exist_ok=True)
LOGO = '<svg viewBox="0 0 32 32" role="img" aria-label="ClutchIQ logo"><rect width="32" height="32" rx="8" fill="currentColor"/><path d="M9 24V10m7 14V8m7 16V10" stroke="var(--bg)" stroke-width="2.6" stroke-linecap="round"/><circle cx="16" cy="5.2" r="2.4" fill="var(--accent)"/></svg>'
ICON = lambda p: f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'
NAV = [("Method", "/methodology"), ("Pricing", "/pricing"), ("Contact", "/contact")]
PAGES = []
def page(slug, title, desc, body, kw="", script="", noindex=False, crumbs=None, ld=None, main_cls=""):
    url = f"{SITE}/{slug}" if slug else SITE + "/"
    full = f"{title} | {NAME}" if slug else title
    if not noindex and slug not in ("404",): PAGES.append(dict(u="/" + slug, t=title, d=desc, k=kw))
    bc = ""
    if crumbs:
        items = [("Home", "/")] + crumbs
        bc = '<nav class="crumbs wrap" aria-label="Breadcrumb">' + "".join(f'<span><a href="{u}">{t}</a></span>' if u else f'<span aria-current="page">{t}</span>' for t, u in items) + "</nav>"
        ld = (ld or []) + [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t, "item": SITE + (u or "/" + slug)} for i, (t, u) in enumerate(items)]}]
    ldj = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in (ld or []))
    robots = '<meta name="robots" content="noindex,nofollow">' if noindex else ""
    nav = "".join(f'<a href="{u}"{" aria-current=page" if u == "/" + slug else ""}>{t}</a>' for t, u in NAV)
    wa = f'<a class="wa" href="https://wa.me/{WA}?text=Hi%20ClutchIQ" aria-label="Chat on WhatsApp" rel="noopener" target="_blank">{ICON("<path d=\"M21 11.5a8.5 8.5 0 0 1-12.6 7.4L3 20l1.2-5.2A8.5 8.5 0 1 1 21 11.5z\"/>")}</a>' if WA else ""
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{full}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">{robots}
<meta name="theme-color" content="#14342b"><meta name="author" content="{OWNER}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{full}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/assets/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="ClutchIQ: ranking cricketers who deliver under pressure">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE}/assets/og.png">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/og.png">
<script>try{{var t=localStorage.getItem("ciq-theme")||(matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light");document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="stylesheet" href="/assets/style.css">{ldj}</head><body>
<a class="skip" href="#main">Skip to content</a><div id="progress" role="presentation"></div>
<header class="site"><div class="wrap bar"><a class="logo" href="/" aria-label="ClutchIQ home">{LOGO}{NAME}</a>
<nav class="main" aria-label="Main">{nav}<a href="/dashboard">Rankings</a></nav>
<div class="tools"><div class="search"><input id="q" type="search" placeholder="Search" aria-label="Search the site" autocomplete="off"><div id="results" role="listbox"></div></div>
<button class="icon" id="theme" aria-label="Toggle dark mode">{ICON('<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>')}</button>
<a class="btn sm" id="authlink" href="/login">Log in</a><button class="icon" id="burger" aria-label="Menu" aria-expanded="false">{ICON('<path d="M4 7h16M4 12h16M4 17h16"/>')}</button></div></div></header>
{bc}<main id="main" class="{main_cls}">{body}</main>
<footer class="site"><div class="wrap"><div class="fgrid"><div><a class="logo" href="/">{LOGO}{NAME}</a><p class="upd">Clutch performance, measured from ball-by-ball data. Built for SupeRR Selector Season 2.</p></div>
<div><h3>Product</h3><ul><li><a href="/methodology">Methodology</a></li><li><a href="/dashboard">Rankings</a></li><li><a href="/pricing">Pricing</a></li><li><a href="/contact">Contact</a></li></ul></div>
<div><h3>Legal</h3><ul><li><a href="/privacy">Privacy policy</a></li><li><a href="/terms">Terms and conditions</a></li><li><a href="/cookies">Cookie policy</a></li><li><a href="/payment-terms">Payment terms</a></li></ul></div></div>
<div class="copy"><span>&copy; {TODAY.year} {OWNER}. All rights reserved.</span><span><a href="mailto:{EMAIL}">{EMAIL}</a> &middot; Last updated {UPD}</span></div></div></footer>
<div class="fab">{wa}<a href="/contact" aria-label="Contact us">{ICON('<path d="M4 5h16v11H8l-4 4z"/>')}</a><button id="top" aria-label="Back to top">{ICON('<path d="M12 19V5m-6 6 6-6 6 6"/>')}</button></div>
<div id="cookie" role="dialog" aria-label="Cookie notice"><p>We use one essential cookie to keep you signed in. With your OK we also use analytics cookies. <a href="/cookies">Cookie policy</a></p><div><button class="btn sm" data-consent="yes">Accept</button><button class="btn sm ghost" data-consent="no">Essential only</button></div></div>
<dialog id="modal"><p id="modal-msg"></p><menu><button class="btn sm ghost" id="modal-no" style="width:auto;margin:0">Cancel</button><button class="btn sm" id="modal-yes" style="width:auto;margin:0">Confirm</button></menu></dialog><div id="toast" role="status" aria-live="polite"></div>
<script src="/assets/search.js"></script><script src="/assets/app.js" defer></script>{f'<script src="/assets/{script}" defer></script>' if script else ""}</body></html>'''
    (P / (slug + ".html" if slug else "index.html")).write_text(html)

def legal(slug, title, desc, inner):
    page(slug, title, desc, f'<article class="narrow prose" style="padding:2rem 0"><h1>{title}</h1><p class="upd">Last updated {UPD}</p>{inner}</article>', crumbs=[(title, None)], kw="legal policy")
def form(api, fields, btn, redirect="", extra=""):
    return f'<form data-api="{api}" {f"data-redirect={redirect}" if redirect else ""} novalidate>{fields}<div class="form-error" role="alert" hidden></div><div class="form-ok" role="status" hidden></div><button class="btn" type="submit">{btn}</button></form>{extra}'
F = lambda n, l, t="text", a="", h="": f'<label for="{n}">{l}</label><input id="{n}" name="{n}" type="{t}" {a} required>{f"<p class=hint>{h}</p>" if h else ""}'
PWH = "At least 8 characters with upper case, lower case and a number."
def auth(slug, title, desc, h, sub, inner):
    page(slug, title, desc, f'<section class="auth"><div class="card"><h1 style="font-size:1.9rem">{h}</h1><p class="hint">{sub}</p><div id="notice" class="notice"></div>{inner}</div></section>', noindex=True)

top = lambda L: "".join(f'<li><b>{r["rank"]}. {r["name"]}</b><small>{r["pressure_balls"]} pressure balls</small></li>' for r in L[:3])
FAQ = [("What counts as pressure?", f"Every delivery gets a pressure score from 0 to 1 using the required run rate, wickets lost, how late in the innings it is and whether the match is a knockout. The top 20 percent of deliveries (score of {M['threshold']} or more) are treated as pressure situations."),
 ("Which data is used?", f"{M['matches']} IPL and T20I matches from 2022 onwards, covering {M['deliveries']:,} deliveries."),
 ("How are players compared fairly?", "Each ball is compared with the league average for the same format, innings and phase, so openers and finishers are not judged against the same yardstick. Small samples are shrunk towards zero."),
 ("Do I need an account?", "The top three in each list are public. Create a free account to see the full top 25 batters and bowlers."),
 ("Can I copy the rankings?", "Yes. The dashboard has a copy button for each top 10 list.")]
faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
hero_svg = '<svg viewBox="0 0 420 340" role="img" aria-label="Chart showing a batter scoring faster as pressure rises, beside three cricket stumps"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><path d="M30 300h360" opacity=".3"/><path d="M60 270 150 220l70 25 90-95 70-80" stroke="var(--accent)" stroke-width="5"/></g><g fill="currentColor"><circle cx="60" cy="270" r="6"/><circle cx="150" cy="220" r="6"/><circle cx="220" cy="245" r="6"/><circle cx="310" cy="150" r="6"/><circle cx="380" cy="70" r="9" fill="var(--accent)"/></g><g stroke="currentColor" stroke-width="7" stroke-linecap="round"><path d="M70 120V40M100 120V40M130 120V40"/></g><path d="M66 36h68" stroke="var(--accent)" stroke-width="6" stroke-linecap="round"/></svg>'
home = f'''<div class="wrap"><section class="hero"><div><p class="eyebrow">Clutch performance analytics</p><h1>Find the players who rise when the game is on the line.</h1>
<p class="lead">ClutchIQ scores every ball of IPL and T20I cricket for pressure, then ranks batters and bowlers on how they perform against what is normal for them.</p>
<div class="cta"><a class="btn" href="/signup">Create free account</a><a class="btn ghost" href="/methodology">Read the method</a></div></div><div>{hero_svg}</div></section>
<div class="stats"><div class="stat"><b>{M['matches']}</b><span>matches analysed</span></div><div class="stat"><b>{M['deliveries']:,}</b><span>deliveries scored</span></div><div class="stat"><b>{M['pressure_deliveries']:,}</b><span>pressure deliveries</span></div><div class="stat"><b>{M['eligible_batters']+M['eligible_bowlers']}</b><span>rated players</span></div></div>
<section class="block"><h2>How it works</h2><div class="grid3"><div class="card"><span class="num">01</span><h3>Score the situation</h3><p>Required rate, wickets in hand, balls left and match stage combine into one pressure score for each delivery.</p></div><div class="card"><span class="num">02</span><h3>Compare with the norm</h3><p>Runs and wickets are measured against the league average for the same format, innings and phase.</p></div><div class="card"><span class="num">03</span><h3>Rank the reliable</h3><p>Impact, consistency across matches and lift over the player’s own baseline decide the order.</p></div></div></section>
<section class="block"><h2>Current leaders</h2><div class="grid2"><div class="card"><h3>Batters</h3><ol class="top">{top(R['batters'])}</ol></div><div class="card"><h3>Bowlers</h3><ol class="top">{top(R['bowlers'])}</ol></div></div><p class="cta"><a class="btn" href="/dashboard">See the full top 25</a></p></section>
<section class="block narrow" style="margin:0 auto"><h2>Frequently asked questions</h2>{faq}</section></div>'''
page("", "ClutchIQ: Cricket Players Who Perform Under Pressure", "ClutchIQ ranks IPL and T20I batters and bowlers by how they perform in high-pressure situations, using ball-by-ball data from 2022.", home, kw="home cricket pressure ranking",
     ld=[{"@context": "https://schema.org", "@type": "Organization", "name": NAME, "url": SITE, "logo": SITE + "/assets/favicon.svg", "email": EMAIL, "founder": {"@type": "Person", "name": OWNER}},
         {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE},
         {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}])

page("methodology", "Methodology", "How ClutchIQ defines pressure, rates batters and bowlers against their own baselines, and keeps small samples from distorting the rankings.",
f'''<article class="narrow prose" style="padding:2rem 0"><h1>Methodology</h1><p class="upd">Last updated {UPD}</p>
<h2>1. Pressure index</h2><p>For every delivery we compute a score from 0 to 1 from the state of the innings before the ball.</p>
<ul><li><b>Chasing:</b> 0.55 × required-rate stress (required rate above 7.5, capped at 13.5) + 0.25 × wickets lost ÷ 10 + 0.20 × share of the innings gone.</li><li><b>Batting first:</b> 0.6 × (half wickets lost + half share of innings gone), because there is no target to chase.</li><li><b>Knockout matches</b> add 0.1.</li></ul>
<p>A delivery counts as a pressure situation when its score is in the top 20 percent ({M['threshold']} or higher). That gives {M['pressure_deliveries']:,} pressure deliveries out of {M['deliveries']:,}.</p>
<h2>2. Does it separate pressure from ordinary play?</h2><div class="tw"><table><thead><tr><th>Situation</th><th>Runs per ball</th><th>Wicket rate</th><th>Balls</th></tr></thead><tbody><tr><td>Ordinary</td><td>{M['compare']['False']['runs_per_ball']:.2f}</td><td>{M['compare']['False']['wicket_rate']*100:.1f}%</td><td>{M['compare']['False']['balls']:,}</td></tr><tr><td>Pressure</td><td>{M['compare']['True']['runs_per_ball']:.2f}</td><td>{M['compare']['True']['wicket_rate']*100:.1f}%</td><td>{M['compare']['True']['balls']:,}</td></tr></tbody></table></div><p>Wickets fall about 64 percent more often under pressure, so the index picks out genuinely harder moments.</p>
<h2>3. Performance measure</h2><p>Each ball gets an <b>impact</b> value against the league average for the same format (IPL-style league or T20I), innings and phase (powerplay, middle, death), calculated separately for pressure and ordinary balls. A wicket is valued at {M['wicket_value']:.0f} runs.</p>
<ul><li><b>Batters:</b> (runs − expected runs) − {M['wicket_value']:.0f} × (dismissed − expected dismissal rate). Wides are excluded.</li><li><b>Bowlers:</b> (expected runs conceded − runs conceded, including wides and no-balls) + {M['wicket_value']:.0f} × (wicket − expected wicket rate). Run-outs are not credited.</li></ul>
<h2>4. Rating and fairness</h2><ul><li><b>Eligibility:</b> at least 120 pressure balls and 15 matches with 6 or more pressure balls. {M['eligible_batters']} batters and {M['eligible_bowlers']} bowlers qualify.</li><li><b>Shrinkage:</b> impact per 100 balls is multiplied by n ÷ (n + {M['shrink_k']}) so short spells cannot dominate.</li><li><b>Rating</b> = 0.60 × z(shrunk impact) + 0.25 × z(consistency, the share of matches with positive impact) + 0.15 × z(lift over the player’s own non-pressure baseline).</li><li><b>IPL and T20I</b> are pooled, but expectations are set within each format so neither inflates the other.</li></ul>
<h2>5. Limitations</h2><p>Strict eligibility leaves a modest batter pool. Weights, the 80th-percentile cut-off and the wicket value are judgement calls and are fixed in <code>analysis/pressure_model.py</code>. Opposition quality, venue and batting order are not adjusted for. Super overs are excluded.</p></article>''',
crumbs=[("Methodology", None)], kw="pressure index method rating")

page("pricing", "Pricing", "ClutchIQ is free to use. Paid plans for exports and team tools are planned; see how early access works.",
f'''<div class="wrap" style="padding:2rem 0"><h1>Pricing</h1><p class="lead upd">Everything you need to explore the rankings is free.</p><div class="grid2"><div class="card"><h3>Free</h3><p style="font:700 2.2rem var(--serif);margin:0">₹0</p><ul><li>Full top 25 batters and bowlers</li><li>Methodology and pressure comparison</li><li>Copy top 10 lists</li></ul><a class="btn" href="/signup">Create account</a></div>
<div class="card"><h3>Pro (early access)</h3><p style="font:700 2.2rem var(--serif);margin:0">Coming soon</p><ul><li>CSV export of every rated player</li><li>Custom pressure thresholds</li><li>Team and franchise comparisons</li></ul><a class="btn ghost" href="/contact">Request early access</a></div></div><p class="upd" style="margin-top:1.5rem">No payment is taken on this site today. Future paid plans will follow our <a href="/payment-terms">payment terms</a>.</p></div>''',
crumbs=[("Pricing", None)], kw="plans price payment")

page("contact", "Contact", f"Contact ClutchIQ. Send a message or email {EMAIL}.", f'''<div class="narrow" style="padding:2rem 0"><h1>Contact us</h1><p>Questions, feedback or early-access requests? Write to <a href="mailto:{EMAIL}">{EMAIL}</a> or use the form.</p><div class="card">{form("/api/contact", F("name","Your name",a='autocomplete=name maxlength=80')+F("email","Email","email",'autocomplete=email maxlength=120')+'<label for="message">Message</label><textarea id="message" name="message" rows="5" minlength="10" maxlength="2000" required></textarea>', "Send message")}</div></div>''',
crumbs=[("Contact", None)], kw="support email message", ld=[{"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact ClutchIQ", "url": SITE + "/contact"}])

auth("login", "Log in", "Log in to ClutchIQ to view the full pressure rankings.", "Welcome back", "Log in to see the full rankings.",
 form("/api/auth/login", F("email","Email","email","autocomplete=email")+F("password","Password","password","autocomplete=current-password"), "Log in", "/dashboard", '<p class="alt"><a href="/forgot-password">Forgot password?</a></p><p class="alt">New here? <a href="/signup">Create an account</a></p>'))
auth("signup", "Create account", "Create a free ClutchIQ account to unlock the full top 25 batters and bowlers.", "Create your account", "Free, and it takes under a minute.",
 form("/api/auth/signup", F("name","Full name","text","autocomplete=name maxlength=80")+F("email","Email","email","autocomplete=email")+F("password","Password","password","autocomplete=new-password minlength=8",PWH)+F("confirmPassword","Confirm password","password","autocomplete=new-password")+'<label style="font-weight:400"><input type="checkbox" name="agree" value="1" required style="width:auto"> I agree to the <a href="/terms">Terms</a> and <a href="/privacy">Privacy policy</a></label>', "Create account", "/login?registered=1", '<p class="alt">Already registered? <a href="/login">Log in</a></p>'))
auth("forgot-password", "Forgot password", "Request a ClutchIQ password reset link.", "Reset your password", "Enter your email and we will send a reset link that works once for 30 minutes.",
 form("/api/auth/forgot", F("email","Registered email","email","autocomplete=email"), "Send reset link", "", '<p class="alt"><a href="/login">Back to log in</a></p>'))
auth("reset", "Set a new password", "Choose a new ClutchIQ password.", "Choose a new password", "Reset links are single-use.",
 form("/api/auth/reset", '<input type="hidden" name="token">'+F("password","New password","password","autocomplete=new-password minlength=8",PWH)+F("confirmPassword","Confirm new password","password","autocomplete=new-password"), "Update password", "/login?reset=1"))

page("dashboard", "Dashboard", "Full ClutchIQ pressure rankings for IPL and T20I batters and bowlers.", f'''<div class="wrap" style="padding:2rem 0"><div style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;align-items:center"><div><p class="eyebrow">Dashboard</p><h1 style="margin:0">Hello, <span id="who">…</span></h1></div><button class="btn ghost sm" style="width:auto" data-confirm="Log out of ClutchIQ?" data-action="logout">Log out</button></div>
<div class="tabs" role="tablist"><button data-tab="batters" role="tab" aria-selected="true">Batters</button><button data-tab="bowlers" role="tab" aria-selected="false">Bowlers</button></div>
<div id="board"><div class="skel"></div><div class="skel"></div><div class="skel"></div><div class="skel"></div></div>
<div class="grid2" style="margin-top:1.5rem"><div class="card"><h3>Top 10 (copy for your submission)</h3><textarea id="top10" rows="10" readonly aria-label="Top 10 list"></textarea><button class="btn sm" style="margin-top:.8rem" data-copy="#top10">Copy top 10</button></div>
<div class="card"><h3>Pressure vs ordinary play</h3><div class="tw"><table style="min-width:0"><thead><tr><th>Situation</th><th>Runs/ball</th><th>Wicket rate</th><th>Balls</th></tr></thead><tbody id="cmp"></tbody></table></div><p class="hint">Rating blends shrunk impact (60%), consistency (25%) and lift over baseline (15%). See the <a href="/methodology">methodology</a>.</p></div></div></div>''', script="dashboard.js", noindex=True)

pp = lambda s: "".join(f"<h2>{h}</h2>{t}" for h, t in s)
legal("privacy", "Privacy Policy", "How ClutchIQ collects, uses and protects your personal information.", pp([
("Who we are", f"ClutchIQ is operated by {OWNER}, India. Contact: <a href='mailto:{EMAIL}'>{EMAIL}</a>."),
("What we collect", "<ul><li><b>Account data:</b> name, email address and a password hash (we never store your password).</li><li><b>Contact messages:</b> name, email and message text.</li><li><b>Campaign data:</b> UTM parameters from the link you arrived through, saved with your account.</li><li><b>Technical data:</b> IP address, used briefly for rate limiting and security.</li><li><b>Analytics:</b> anonymised usage data, only if you accept analytics cookies.</li></ul>"),
("How we use it", "To run your account, secure the service, answer messages, send password-reset emails and improve the product. We do not sell personal data."),
("Where it is stored", "Data is stored in a Neon PostgreSQL database. The site is hosted on Vercel. Emails are sent through our email provider. These providers process data on our behalf."),
("Retention and your rights", f"We keep account data until you ask us to delete it. You may request access, correction or deletion at any time by emailing <a href='mailto:{EMAIL}'>{EMAIL}</a>. We respond within 30 days, in line with India’s Digital Personal Data Protection Act, 2023."),
("Children", "ClutchIQ is not intended for children under 13 and we do not knowingly collect their data."),
("Changes", "We will update this page and its date when this policy changes.")]))
legal("terms", "Terms and Conditions", "The terms that apply when you use ClutchIQ.", pp([
("Acceptance", "By creating an account or using ClutchIQ you agree to these terms."),
("Your account", "Provide accurate details, keep your password secret and tell us about any unauthorised use. You are responsible for activity on your account."),
("Acceptable use", "Do not attack, overload, scrape at scale or attempt to access the service or other users’ data without permission."),
("Content and data", f"Rankings are statistical analysis of public match data and are provided for information only. We do not guarantee accuracy or fitness for betting, selection or any decision. The ClutchIQ name, design and code are &copy; {TODAY.year} {OWNER}."),
("Termination", "We may suspend accounts that break these terms. You may delete your account by emailing us."),
("Liability", "To the extent permitted by law, the service is provided as is and we are not liable for indirect or consequential loss."),
("Governing law", f"These terms are governed by the laws of India. Questions: <a href='mailto:{EMAIL}'>{EMAIL}</a>.")]))
legal("cookies", "Cookie Policy", "Which cookies and local storage ClutchIQ uses and how to control them.", pp([
("Essential", "<div class='tw'><table style='min-width:0'><thead><tr><th>Name</th><th>Purpose</th><th>Duration</th></tr></thead><tbody><tr><td>session</td><td>Keeps you signed in (HttpOnly, Secure)</td><td>7 days</td></tr><tr><td>ciq-consent</td><td>Remembers your cookie choice</td><td>Until cleared</td></tr><tr><td>ciq-theme</td><td>Remembers light or dark mode</td><td>Until cleared</td></tr><tr><td>ciq-utm</td><td>Remembers the campaign link you arrived from</td><td>Until cleared</td></tr></tbody></table></div>"),
("Analytics", "Google Analytics cookies are set only if you choose Accept. Choosing Essential only keeps them off."),
("Changing your choice", "Clear this site’s storage in your browser and the banner will appear again.")]))
legal("payment-terms", "Payment Terms", "Payment, refund and billing terms for paid ClutchIQ plans.", pp([
("Current status", "ClutchIQ is free today and no payment is collected. These terms apply once paid plans launch."),
("Prices and taxes", "Prices are shown in Indian rupees and include applicable GST unless stated."),
("Payment processing", "Payments are handled by a third-party processor. We never see or store your card, UPI or bank details."),
("Billing", "Plans are charged in advance for the period shown. Failed payments may lead to access being paused."),
("Cancellation and refunds", f"Cancel any time to stop renewal. If you are unhappy, email <a href='mailto:{EMAIL}'>{EMAIL}</a> within 7 days of a charge for a full refund."),
("Disputes", "Contact us first so we can fix billing issues quickly. These terms follow our <a href='/terms'>Terms and Conditions</a>.")]))
page("404", "Page not found", "The page you are looking for does not exist. Return to the ClutchIQ home page.", '<section class="narrow" style="padding:5rem 0;text-align:center"><p class="eyebrow">Error 404</p><h1>Bowled out: page not found</h1><p>The page may have moved or never existed.</p><div class="cta" style="justify-content:center"><a class="btn" href="/">Back to home</a><a class="btn ghost" href="/contact">Report a problem</a></div></section>', noindex=True)

# assets & SEO files
(P / "assets/favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#14342b"/><path d="M9 24V10m7 14V8m7 16V10" stroke="#f6f1e7" stroke-width="2.6" stroke-linecap="round"/><circle cx="16" cy="5.2" r="2.4" fill="#e0775f"/></svg>')
(P / "assets/search.js").write_text("window.CIQ_PAGES=" + json.dumps(PAGES) + ";" + (f'window.CIQ_GA="{GA}";' if GA else ""))
idx = [p for p in PAGES]
(P / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{SITE}{p['u'] if p['u']!='/' else '/'}</loc><lastmod>{ISO}</lastmod></url>" for p in [dict(u="/")] + [x for x in idx if x["u"] != "/"]) + "</urlset>")
(P / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /dashboard\nDisallow: /reset\n\nSitemap: {SITE}/sitemap.xml\n")
(P / "llms.txt").write_text(f"# {NAME}\n\n> ClutchIQ ranks IPL and T20I batters and bowlers by performance under pressure, using ball-by-ball data from 2022.\n\n- [Home]({SITE}/): overview and top three players\n- [Methodology]({SITE}/methodology): pressure index, ratings, limitations\n- [Pricing]({SITE}/pricing): free plan and planned Pro plan\n- [Contact]({SITE}/contact): {EMAIL}\n- [Privacy]({SITE}/privacy), [Terms]({SITE}/terms), [Cookies]({SITE}/cookies), [Payment terms]({SITE}/payment-terms)\n")
from PIL import Image, ImageDraw, ImageFont
im = Image.new("RGB", (1200, 630), "#14342b"); d = ImageDraw.Draw(im)
def fnt(s):
    for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"):
        try: return ImageFont.truetype(f, s)
        except Exception: pass
    return ImageFont.load_default()
for x in (90, 150, 210): d.rounded_rectangle([x, 150, x + 16, 330], 8, fill="#f6f1e7")
d.rounded_rectangle([80, 135, 236, 150], 7, fill="#e0775f")
d.line([(420, 470), (560, 400), (680, 430), (820, 330), (1000, 230)], fill="#e0775f", width=10, joint="curve")
d.text((80, 390), "ClutchIQ", font=fnt(110), fill="#f6f1e7"); d.text((84, 530), "Who delivers when it matters most", font=fnt(40), fill="#d8cfb8")
im.save(P / "assets/og.png", optimize=True)
print("built", len(PAGES), "pages for", SITE)
