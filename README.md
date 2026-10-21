# truesquareremodel.com

Static site. Cloudflare Pages deploys every push to `main` automatically.
- Output directory: `public` (no build command).
- Edit content in `tools/build.py` and `tools/content/`, then run `python3 tools/build.py`, commit, push.
- Shared styles: `public/css/site.css`. Shared script and SETTINGS (webhook, Pixel, GTM): `public/js/site.js`.
