# Tangent website

The public website for **Tangent Fitness & Wellness**, an Android app by
MD AYUB MONDAL. It carries the pages Google Play requires a public URL for.

**Live site:** https://solidtv100-afk.github.io/tangent-website/

| Page | URL |
|---|---|
| Home | `/` |
| Privacy Policy | `/privacy/` |
| Data Safety | `/data-safety/` |
| Terms of Service | `/terms/` |
| Health & Fitness Disclaimer | `/disclaimer/` |
| Delete your data | `/delete-data/` |
| Contact & Support | `/support/` |

## What this repository contains

Static HTML and one stylesheet. No framework, no JavaScript, no web fonts, and
no build step at deploy time — the `.html` files are committed and ready to
serve. The whole site is about 200 KB.

**It contains no Android source code, no database, no keystore and no
credentials.** This repository is public; the app's own repository is separate
and private.

## Editing

`_tools/build.py` generates the pages from one template, so the header,
navigation and footer are written once instead of seven times. Make content
changes there, not in the generated HTML:

```bash
python3 _tools/build.py        # regenerate all pages
python3 _tools/check_links.py  # confirm no internal link 404s
```

CI fails if the committed HTML no longer matches the generator.

## Accuracy rule

Every factual claim about the app was read out of the app's source or its
merged release manifest — the permission list, the absence of the internet
permission, the library list, what the local database stores, how export and
text-to-speech behave.

**Do not add a privacy, security or feature claim that cannot be checked
against the app's code.** The Data Safety page deliberately states what is
*not* claimed (no independent audit, no compliance certification, no separate
database encryption) because an unverifiable reassurance is worse than none.

If the app gains an online feature, update `/privacy/` and `/data-safety/`
*before* that version ships, and change the Play Console Data safety form to
match.

## Changing the URL

`BASE_URL` at the top of `_tools/build.py` feeds the canonical links, the Open
Graph URLs and the sitemap. Change it there and re-run the generator; every
in-page link is relative, so nothing else needs touching.

---

Developer: MD AYUB MONDAL · Support: solid.tv.100@gmail.com
