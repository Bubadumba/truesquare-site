# truesquareremodel.com

Static site of TrueSquare Remodel LLC (Seattle bathroom and kitchen remodeling, WA L&I # TRUESRL759QK).
`tools/build.py` renders the main pages, `tools/build_blog.py` renders the blog; both write finished HTML into
`public/`, which Cloudflare Pages deploys from `main` with no build command. Generated HTML is committed.
`main` is protected by the ruleset `protect-main`: never push to `main`, open Pull Requests with `gh api`, never merge.

## Commands
```
pip install -r tools/requirements.txt
python3 tools/validate_content.py      # articles follow the rules (CI runs this)
python3 tools/build_all.py             # build.py + build_blog.py: pages, blog, sitemap, _redirects (CI checks the output is identical)
python3 tools/generate_image.py --help # illustrations via the OpenAI Images API (see content/image-style.md)
```

## Who edits what
- The content agent (skill `.claude/skills/seo-article/SKILL.md`, critic `.claude/agents/article-critic.md`) edits ONLY
  `content/**`, `public/blog/**`, `public/img/blog/ai/**`, `public/sitemap.xml`, `public/_redirects`; the last four only
  through the build scripts. CI job `scope` fails an agent branch that touches anything else.
- The owner edits everything else: `tools/`, `public/css`, `public/js`, main pages, workflows, `.claude/`, this file.
  Ad landing pages come from `tools/build_lp.py` / `tools/build_lp_v3.py` (not part of CI's rebuild check). Blog-only styles
  live in `public/css/blog.css`, inlined on blog pages by `build_blog.py`; `site.css` is inlined on every page by `build.py`.
- Real photos: the owner adds them under `public/img/blog/` and registers them in `content/photos.json`
  (`content/photos.schema.md`). Generated illustrations go under `public/img/blog/ai/` via the script only.

## Articles
Markdown with YAML frontmatter in `content/blog/<slug>.md`. Only Markdown plus five blocks:
```
:::costtable                      YAML: title, updated, note, rows: [{item, low, high, note}]
:::
{{photo id="b13" caption="What is shown." alt="One factual sentence" size="full|half"}}
:::callout tip                    note | warning | tip | owner ("From our jobs")
Markdown
:::
{{cta}}
:::faq                            YAML list of {q, a}
:::
```
No raw HTML, no `![image]`, no H1 in the body, no em or en dashes, nothing from `tools/banned-terms.txt`.

## Images (five rules)
1. Default 2 images per article (hero included); up to 6 only when each extra one explains a step, a diagram, a variant or a material detail, with a one-line reason in the PR.
2. Real photos first: `clientConsent: true`, at most 2 posts per photo, a hero photo is unique on the site.
3. Nothing fits: generate with `tools/generate_image.py` following `content/image-style.md`, look at all candidates, keep one.
4. Generated images never in project stories, never in before/after pairs, never with "our / we / project / job", a client name or a city in the caption, alt or surrounding sentence.
5. No visible AI label (owner decision 2026-10-24); `source: "ai"` in photos.json and the IPTC tag stay.

## Hard rules (verbatim from the setup spec)
2. Hard-code only facts that are already in the repository: company "TrueSquare Remodel LLC"; owner "Serhii Tomilov"; WA L&I registration "TRUESRL759QK" and its verify link; phone +1 206-222-2328; email info@truesquareremodel.com; "Seattle, WA"; the services in `NAV_SERVICES`; the Google Business Profile and Thumbtack links; the 12 cities in `CITIES` (as service areas only, never as "cities with completed projects"). Every other fact (years in business, bond and insurance amounts, review counts, prices, projects, certifications) comes from `content/business-facts.md` or is written as `⬜ FILL`. Never invent any of it. Phone numbers only in full +1 XXX-XXX-XXXX form.
3. Never write the words financing, "financing available", credit, loan, APR, "subject to credit approval". Never write "in-house" for trades: the approved wording is "our crew".
4. Do not create city or neighborhood pages.
5. Publishing an article, referencing a photo, generating an illustration or adding a 301 must never require touching `tools/`, `public/css`, `public/js`, workflows or other pages.
6. Default publishing mode is manual review: `content/config.yaml` has `auto_publish: false`. Nothing deploys without a human merge.
