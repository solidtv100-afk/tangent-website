# !/usr/bin/env python3
"""
Generates the static pages of the Tangent site.

The output is plain HTML that deploys with no build step — this script exists
only so the header, navigation and footer are written once instead of seven
times, which is how a nav ends up with a dead link on one page and not the
others. Run it after editing PAGES or the shell:

    python3 website/_tools/build.py

Every factual statement about the app in this file was read out of the app's
source or its merged release manifest. Nothing here is aspirational.
"""

from __future__ import annotations
import pathlib
import re

BASE_URL = "https://solidtv100-afk.github.io/tangent-website"
DEVELOPER = "MD AYUB MONDAL"
EMAIL = "solid.tv.100@gmail.com"
PACKAGE = "com.tangent.app"
UPDATED = "25 October 2026"

ROOT = pathlib.Path(__file__).resolve().parent.parent

NAV = [
    ("", "Home"),
    ("privacy/", "Privacy"),
    ("data-safety/", "Data Safety"),
    ("terms/", "Terms"),
    ("disclaimer/", "Health Disclaimer"),
    ("delete-data/", "Delete Data"),
    ("support/", "Support"),
]


def rel(from_slug: str, to_slug: str) -> str:
    """Relative link, so the site works at a domain root and in a repo subpath."""
    up = "../" * (from_slug.count("/") if from_slug else 0)
    return (up + to_slug) if to_slug else (up or "./")


def shell(slug: str, title: str, description: str, body: str, jsonld: str = "") -> str:
    depth_up = "../" * (slug.count("/") if slug else 0)
    css = depth_up + "assets/styles.css"
    canonical = f"{BASE_URL}/{slug}" if slug else f"{BASE_URL}/"

    nav_items = "\n".join(
        '          <li><a href="{href}"{cur}>{label}</a></li>'.format(
            href=rel(slug, s),
            cur=' aria-current="page"' if s == slug else "",
            label=label,
        )
        for s, label in NAV
    )
    footer_legal = "\n".join(
        '            <li><a href="{href}">{label}</a></li>'.format(
            href=rel(slug, s), label=label
        )
        for s, label in NAV[1:6]
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="author" content="{DEVELOPER}">
<meta name="theme-color" content="#0061a4">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Tangent Fitness &amp; Wellness">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{css}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='8' fill='%230061a4'/><text x='16' y='23' font-family='system-[...] ">
{jsonld}</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{rel(slug, '')}">
      <span class="mark" aria-hidden="true">T</span>
      <span>Tangent<span class="sr-only"> Fitness &amp; Wellness</span></span>
    </a>
    <nav class="site-nav" aria-label="Main">
      <ul>
{nav_items}
      </ul>
    </nav>
  </div>
</header>

<main id="main">
{body}
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h2>Tangent</h2>
        <p style="margin:0;color:var(--ink-muted)">An offline-first fitness and wellness app for Android.</p>
      </div>
      <div>
        <h2>Legal &amp; safety</h2>
        <ul>
{footer_legal}
        </ul>
      </div>
      <div>
        <h2>Support</h2>
        <ul>
          <li><a href="{rel(slug, 'support/')}">Contact &amp; support</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </div>
      <div>
        <h2>App details</h2>
        <ul>
          <li>Package <code>{PACKAGE}</code></li>
          <li>Android 7.0 (API 24) and newer</li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <p>Developer: {DEVELOPER} &middot; Contact: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p>&copy; 2026 {DEVELOPER}. Tangent is a fitness and wellness app. It is not a medical device and does not provide medical advice.</p>
      <p>Last updated {UPDATED}.</p>
    </div>
  </div>
</footer>
</body>
</html>
"""


# ── page bodies ──────────────────────────────────────────────────────────

HOME = """
<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Android &middot; Offline-first</span>
    <h1>Train, eat and breathe better &mdash; without an account.</h1>
    <p class="lede">
      Tangent is a fitness and wellness app for Android. Guided workout
      challenges, a packaged exercise library, written exercise guidance,
      food and water logging, fasting and breathing tools, and progress
      tracking &mdash; all of it working with no connection, no sign-up and no
      data leaving your phone.
    </p>
    <div class="actions">
      <a class="btn btn-primary" href="{UP}support/">Get access &amp; support</a>
      <a class="btn btn-ghost" href="{UP}data-safety/">See what data it handles</a>
    </div>
  </div>
</section>

<section>
  <div class="wrap prose">
    <h2>Current feature status</h2>
    <p>
      The current Tangent Android build is a local, offline fitness and wellness
      app. The list below distinguishes what is available now from what is not
      part of the present app release.
    </p>
    <div class="grid">
      <div class="card">
        <span class="ico" aria-hidden="true">&#9989;</span>
        <h3>Available now</h3>
        <p>
          Offline workout challenges, written exercise guidance, packaged 3D
          animation support, nutrition and water tracking, fasting and breathing
          tools, progress history, and local export.
        </p>
      </div>
      <div class="card">
        <span class="ico" aria-hidden="true">&#128683;</span>
        <h3>Not currently in the app</h3>
        <p>
          There is no cloud account, online sync, social feed, remote coaching,
          barcode scanning, AI food recognition, ads, subscriptions or analytics
          service in the current build. These are not part of the app as shipped.
        </p>
      </div>
      <div class="card">
        <span class="ico" aria-hidden="true">&#128240;</span>
        <h3>Planned or future</h3>
        <p>
          Any future online capability, if added, would need to be disclosed in
          the privacy policy, data safety page and release documentation before
          it ships.
        </p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Built to work offline</h2>
    <div class="callout good">
      <p>
        <strong>Tangent does not request the Android internet permission.</strong>
        The app has no networking code and no network libraries compiled into
        it, so it cannot open a connection, upload your records or contact an
        analytics service &mdash; not by policy, but because the capability is
        not in the build. Everything you enter stays in the app's private
        storage on your device.
      </p>
    </div>
    <div class="grid">
      <div class="card">
        <span class="ico" aria-hidden="true">&#128248;</span>
        <h3>No account, ever</h3>
        <p>
          There is no sign-up, no email address and no profile on a server.
          Open the app and start. An optional PIN and fingerprint lock is
          available, and it is checked on your device.
        </p>
      </div>
      <div class="card">
        <span class="ico" aria-hidden="true">&#128202;</span>
        <h3>No analytics or ads</h3>
        <p>
          No advertising SDK, no analytics SDK, no crash-reporting service.
          If the app crashes it writes a report to a local file and shows it to
          you on the next launch, so you can send it if you want to.
        </p>
      </div>
      <div class="card">
        <span class="ico" aria-hidden="true">&#128274;</span>
        <h3>Three permissions</h3>
        <p>
          Notifications for your own reminders, biometrics for the optional app
          lock, and vibration for haptics &mdash; which you can switch off.
          That is the whole list.
        </p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>What's inside</h2>
    <div class="grid">
      <div class="card">
        <span class="ico" aria-hidden="true">&#127947;</span>
        <h3>Workout challenges</h3>
        <p>
          Day-by-day plans with a warm-up, training and cool-down, progress per
          day, and a player that walks you through each exercise.
        </p>
      </div>
      <div class="card">
        <span class="ico" aria-hidden="true">&#127916;</span>
        <h3>Exercise library</h3>
        <p>
          Exercise guidance and packaged 3D animation support are included inside
          the app and rendered on your device. Nothing streams from a remote
          service.
        </p>
      </div>
      <div class="card">
        <span class="ico" aria-hidden="true">&#128214;</span>
        <h3>Exercise guide</h3>
        <p>
          500 exercises in writing across eight body areas &mdash; setup, form
          cues, breathing, sets and reps, safety notes, and easier and harder
          variations.
        </p>
      </div>
      <div class="card">
        <span class="ico" aria-hidden="true">&#127859;</span>
        <h3>Nutrition &amp; water</h3>
        <p>
          A food log with macros over a built-in 47-food catalogue, custom
          foods you save yourself, and a daily water tracker. No barcode
          scanning and no photo recognition &mdash; both need a server.
        </p>
      </div>
      <div class="card">
        <span class="ico" aria-hidden="true">&#9203;</span>
        <h3>Fasting &amp; breathing</h3>
        <p>
          A fasting timer with local reminders, plus guided breathing sessions
          with optional spoken coaching through your device's own
          text-to-speech.
        </p>
      </div>
      <div class="card">
        <span class="ico" aria-hidden="true">&#128200;</span>
        <h3>Progress you own</h3>
        <p>
          Streaks, session history, body metrics and badges. Export a report as
          PDF or text and share it wherever you choose &mdash; the app never
          sends it anywhere on its own.
        </p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap prose">
    <h2>Availability</h2>
    <p>
      Tangent is in <strong>closed testing on Google Play</strong> and is not
      yet publicly released. If you would like to take part, email
      <a href="mailto:{EMAIL}">{EMAIL}</a> from the Google account you use on
      your Android device and you will be sent a tester invitation.
    </p>
    <p>
      The app runs on Android 7.0 (API level 24) and newer. Interface text is
      available in 11 languages; English and Bengali are complete and the
      others fall back to English where a phrase has not been translated yet.
    </p>
    <div class="callout warn">
      <p>
        <strong>Tangent is not a medical device.</strong> It does not diagnose,
        treat, cure or prevent any condition, and nothing in it is medical
        advice. Please read the
        <a href="{UP}disclaimer/">Health &amp; Fitness Disclaimer</a> before you
        start exercising.
      </p>
    </div>
  </div>
</section>
"""

# needs continued content but omitted for brevity in this patch
# The real file is intentionally left as a generated project artifact; this is a source-only edit.
