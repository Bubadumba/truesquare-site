# truesquareremodel.com

Static site. Cloudflare Pages deploys every push to `main` automatically (output directory `public`, no build command),
so the generated HTML is committed. `main` is protected by the ruleset `protect-main`: every change goes through a
branch and a Pull Request.

## Main pages
- Edit `tools/build.py` and `tools/content/`, then run `python3 tools/build_all.py`, commit, push a branch, open a PR.
- Shared styles: `public/css/site.css`. Shared script and SETTINGS (webhook, Pixel, GTM): `public/js/site.js`.
- Ad landing pages are built separately by `tools/build_lp.py`.

## Blog
- Articles: `content/blog/<slug>.md` (Markdown + YAML frontmatter + five blocks, see `CLAUDE.md`).
- `python3 tools/validate_content.py` checks them; `python3 tools/build_all.py` renders `public/blog/`, `/how-we-write/`,
  `public/sitemap.xml` (honest `lastmod` from `tools/lastmod.json`) and `public/_redirects`.
- Running only `tools/build.py` rebuilds the main pages and updates `tools/lastmod.json`; the sitemap is written by
  `tools/build_blog.py`.
- Facts the articles may use: `content/business-facts.md`. Topic queue: `content/topics.yaml`. Photo library:
  `content/photos.json` (`content/photos.schema.md`). Pipeline settings: `content/config.yaml`.
- The content agent runs as a Claude Code cloud scheduled task (skill `.claude/skills/seo-article/SKILL.md`,
  critic `.claude/agents/article-critic.md`) and opens a PR per article; the owner reviews the Cloudflare preview and merges.
  Fallback runner: `.github/workflows/seo-article.yml` (schedule commented out).
- Dependencies: `pip install -r tools/requirements.txt`.
