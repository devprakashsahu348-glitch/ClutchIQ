# ClutchIQ
Cricket players who perform under pressure: IPL + T20I ball-by-ball analysis with a full-stack site (static pages, Vercel serverless API, Neon Postgres).
&copy; Dev Prakash Sahu. Contact: devprakashsahu348@gmail.com

## Launch for free
1. **GitHub:** create a repo, upload everything in this folder (the `Data Pack` is git-ignored).
2. **Neon:** create a project at neon.tech, open the SQL Editor, run `db/schema.sql`, copy the connection string.
3. **Gmail app password:** Google Account > Security > 2-Step Verification > App passwords. Used to send reset and contact emails.
4. **Vercel:** Import the repo (Framework: Other). Add the variables from `.env.example` under Settings > Environment Variables, then Deploy.
5. **Rebuild with your real URL:** `python build.py https://YOUR-URL [GA_ID] [WHATSAPP_DIGITS]`, commit, push. This sets canonical tags, sitemap, Open Graph URLs, Google Analytics and the WhatsApp button.
6. **Search Console:** add your URL, submit `/sitemap.xml`.

## Re-run the analysis
`pip install pandas numpy pillow` then `python analysis/pressure_model.py "path/to/Data Pack"` and `python build.py`.
