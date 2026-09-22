#!/usr/bin/env python3
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
UPDATED = "22 September 2026"

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
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='8' fill='%230061a4'/><text x='16' y='23' font-family='system-ui,sans-serif' font-size='19' font-weight='700' text-anchor='middle' fill='%23fff'>T</text></svg>">
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


# ── page bodies ──────────────────────────────────────────────────────────────

HOME = """
<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Android &middot; Offline-first</span>
    <h1>Train, eat and breathe better &mdash; without an account.</h1>
    <p class="lede">
      Tangent is a fitness and wellness app for Android. Guided workout
      challenges, a 3D-animated exercise library, a written guide to 500
      exercises, food and water logging, fasting and breathing timers, and
      progress tracking &mdash; all of it working with no connection, no
      sign-up and no data leaving your phone.
    </p>
    <div class="actions">
      <a class="btn btn-primary" href="{UP}support/">Get access &amp; support</a>
      <a class="btn btn-ghost" href="{UP}data-safety/">See what data it handles</a>
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
        <h3>3D exercise library</h3>
        <p>
          161 exercises demonstrated by 160 packaged 3D animation clips,
          rendered on your device. The models ship inside the app; nothing
          streams.
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

PRIVACY = """
<section>
  <div class="wrap prose">
    <h1>Privacy Policy</h1>
    <p class="meta">Last updated {UPDATED} &middot; Applies to the Android app <code>{PACKAGE}</code></p>

    <div class="callout good">
      <p>
        <strong>Short version:</strong> Tangent collects nothing. It has no
        account system, no analytics, no advertising and no server. It does not
        hold the Android internet permission, so it cannot transmit your
        information anywhere. Everything you enter is stored in the app's
        private storage on your own device, and deleting the app deletes it.
      </p>
    </div>

    <h2>1. Who is responsible</h2>
    <p>
      Tangent Fitness &amp; Wellness is developed and published by
      <strong>{DEVELOPER}</strong>, an individual developer. For any privacy
      question, write to <a href="mailto:{EMAIL}">{EMAIL}</a>.
    </p>

    <h2>2. What Tangent does not do</h2>
    <p>
      These statements describe the app as built, and each one can be checked
      against the app's manifest and its dependency list:
    </p>
    <ul>
      <li>
        <strong>It does not request the <code>INTERNET</code> permission.</strong>
        Without that permission Android refuses any network request the app
        might attempt, and the app contains no networking code or network
        libraries in the first place.
      </li>
      <li><strong>It has no user accounts.</strong> No registration, no email address, no password held on a server.</li>
      <li><strong>It contains no analytics or telemetry SDK.</strong> No usage statistics are gathered or sent.</li>
      <li><strong>It contains no advertising SDK</strong> and shows no ads.</li>
      <li><strong>It contains no third-party crash-reporting service.</strong></li>
      <li><strong>It does not use your location.</strong> No location permission is requested.</li>
      <li><strong>It does not access your camera, microphone, contacts, photos, files or call data.</strong> None of those permissions are requested.</li>
      <li><strong>It does not use advertising identifiers</strong> and does not profile or track you.</li>
    </ul>

    <h2>3. What Tangent stores, and where</h2>
    <p>
      The app saves what you put into it so the app can show it back to you.
      All of it lives in a private database inside the app's own storage area,
      which other apps on your device cannot read. It includes:
    </p>
    <ul>
      <li>Your display name, if you enter one, and your chosen fitness level and goal.</li>
      <li>Body metrics you choose to enter, such as height and weight.</li>
      <li>Workout progress: completed days, completion percentages, session history and streaks.</li>
      <li>Food and water entries, saved custom foods, and a calorie budget if you set one.</li>
      <li>Fasting sessions, breathing sessions, journey and wellness progress.</li>
      <li>Settings: interface language, haptics, rest duration, first day of the week.</li>
      <li>If you enable the app lock, a salted cryptographic hash of your PIN &mdash; never the PIN itself.</li>
    </ul>
    <p>
      This information is not transmitted anywhere. There is no cloud sync and
      no backup server, which also means the app cannot restore your history if
      you move to a new phone.
    </p>

    <h2>4. Android backup</h2>
    <p>
      The app declares <code>allowBackup="false"</code>, and its database is
      additionally excluded from Android cloud backup and from device-to-device
      transfer. Your fitness records are therefore not copied into your Google
      account by the operating system.
    </p>

    <h2>5. Permissions, and why each one exists</h2>
    <div class="table-scroll" role="region" aria-label="App permissions" tabindex="0">
      <table>
        <caption>Every permission in the app's release manifest.</caption>
        <thead>
          <tr><th scope="col">Permission</th><th scope="col">Why it is needed</th><th scope="col">Optional?</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><code>POST_NOTIFICATIONS</code></td>
            <td>Shows the reminders you schedule yourself, such as the end of a fast. Android asks your permission the first time and the app works without it.</td>
            <td>Yes</td>
          </tr>
          <tr>
            <td><code>USE_BIOMETRIC</code></td>
            <td>Lets you unlock the optional app lock with a fingerprint instead of your PIN. Your biometric data is handled by Android and is never visible to the app.</td>
            <td>Yes &mdash; only used if you turn the app lock on</td>
          </tr>
          <tr>
            <td><code>VIBRATE</code></td>
            <td>Haptic feedback during workouts and timers. There is a setting to switch it off.</td>
            <td>Yes</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p>
      The app does not request exact-alarm permissions; reminders are scheduled
      inexactly, which means Android may deliver them a little late in order to
      save battery.
    </p>

    <h2>6. Third-party components</h2>
    <p>
      Tangent is built with open-source libraries that render the interface,
      store data locally and draw the 3D exercise animations. None of them
      collects or transmits personal information in this app:
    </p>
    <ul>
      <li>AndroidX and Jetpack Compose (interface), AndroidX Navigation, Core SplashScreen</li>
      <li>AndroidX Room (the local database)</li>
      <li>Kotlin Coroutines</li>
      <li>SceneView, built on Google Filament (renders the packaged 3D models on your device)</li>
    </ul>
    <p>
      There is no Google Analytics, no Firebase, no Google Play Services data
      component, no advertising library and no social-media SDK in the app.
    </p>

    <h2>7. When information leaves your device &mdash; only if you send it</h2>
    <p>Two features can move data off the device, and both require you to act:</p>
    <ul>
      <li>
        <strong>Progress export.</strong> You can export a progress report as a
        PDF or text file. The file is written to the app's temporary storage and
        then handed to Android's share sheet, where <em>you</em> pick the
        destination &mdash; email, a messaging app, your own files. Tangent
        does not choose a destination and does not send anything by itself.
      </li>
      <li>
        <strong>Contacting support.</strong> If you email
        <a href="mailto:{EMAIL}">{EMAIL}</a>, your message and email address
        reach that mailbox, as with any email. Support mail is used only to
        answer you and is not added to any marketing list.
      </li>
    </ul>

    <h2>8. Spoken coaching and text-to-speech</h2>
    <p>
      Optional spoken coaching passes short phrases to the text-to-speech
      engine installed on your device. That engine is part of your Android
      system or a separate app you installed, not part of Tangent, and its own
      privacy behaviour is governed by whoever provides it. Turn spoken coaching
      off if you would rather it were not used.
    </p>

    <h2>9. Crash reports</h2>
    <p>
      If the app crashes, it writes a technical report to a file in its own
      private storage and displays it the next time you open the app so you can
      screenshot it and send it to support if you wish. That file is never
      uploaded and is deleted once it has been shown.
    </p>

    <h2>10. Children</h2>
    <p>
      Tangent is not directed at children and is not designed for use by anyone
      under 13. Because the app collects no information at all, it holds no
      children's data.
    </p>

    <h2>11. Your rights over your data</h2>
    <p>
      Since your information never leaves your device, you already have
      complete control of it: no request to us is required, and there is
      nothing on our side to access, correct, export or erase. To remove
      everything, see <a href="{UP}delete-data/">Delete your data</a>. To take a
      copy with you, use the export feature described above.
    </p>

    <h2>12. Security</h2>
    <p>
      Your records sit in the app's private storage, which Android isolates
      from other apps. You can add a PIN and optional fingerprint lock in the
      app's security settings. Please also protect the device itself with a
      screen lock: on a device with no lock, anyone holding it can open most
      apps. No method of storage is perfectly secure, and we do not claim
      otherwise.
    </p>

    <h2>13. Changes to this policy</h2>
    <p>
      If the app's behaviour changes &mdash; for example if a future version
      adds an online feature &mdash; this page will be updated before that
      version is released, and the date at the top will change. We will not
      quietly begin collecting data under an old policy.
    </p>

    <h2>14. Contact</h2>
    <p>
      {DEVELOPER}<br>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
    </p>
  </div>
</section>
"""


DATA_SAFETY = """
<section>
  <div class="wrap prose">
    <h1>Data Safety</h1>
    <p class="meta">Last updated {UPDATED} &middot; Mirrors the Data safety declaration for <code>{PACKAGE}</code> on Google Play</p>

    <div class="callout good">
      <p>
        <strong>No data collected. No data shared.</strong> In Google Play's
        terms, "collected" means data transferred off your device. Tangent
        transfers nothing off your device, because it does not hold the Android
        internet permission and contains no networking code.
      </p>
    </div>

    <h2>Summary</h2>
    <div class="table-scroll" role="region" aria-label="Data safety summary" tabindex="0">
      <table>
        <thead>
          <tr><th scope="col">Question</th><th scope="col">Answer</th></tr>
        </thead>
        <tbody>
          <tr><td>Does the app collect or share any user data?</td><td><strong>No</strong></td></tr>
          <tr><td>Is data encrypted in transit?</td><td>Not applicable &mdash; no data is transmitted</td></tr>
          <tr><td>Does the app have a way to delete data?</td><td><strong>Yes</strong> &mdash; uninstall, or clear app data (<a href="{UP}delete-data/">instructions</a>)</td></tr>
          <tr><td>Are there ads?</td><td>No</td></tr>
          <tr><td>Are there in-app purchases?</td><td>No</td></tr>
          <tr><td>Does the app use an advertising ID?</td><td>No</td></tr>
          <tr><td>Does the app share data with third parties?</td><td>No</td></tr>
          <tr><td>Has the app been independently security reviewed?</td><td>No &mdash; we make no such claim</td></tr>
        </tbody>
      </table>
    </div>

    <h2>Data the app stores on your device</h2>
    <p>
      Google Play asks separately about data stored only on the device. This is
      what Tangent keeps locally, none of which is collected or shared:
    </p>
    <div class="table-scroll" role="region" aria-label="Data stored on your device" tabindex="0">
      <table>
        <thead>
          <tr><th scope="col">Category</th><th scope="col">What specifically</th><th scope="col">Why</th></tr>
        </thead>
        <tbody>
          <tr>
            <td>Health &amp; fitness</td>
            <td>Workout progress, session history, streaks, fasting and breathing sessions, body metrics you enter, food and water entries</td>
            <td>To show your own history and progress back to you</td>
          </tr>
          <tr>
            <td>Personal info</td>
            <td>A display name, if you choose to enter one</td>
            <td>To greet you in the app</td>
          </tr>
          <tr>
            <td>App preferences</td>
            <td>Language, haptics, rest duration, first day of week, calorie budget</td>
            <td>To remember how you like the app set up</td>
          </tr>
          <tr>
            <td>Security</td>
            <td>A salted hash of your app-lock PIN, if you enable the lock. Never the PIN itself.</td>
            <td>To check the PIN you type without storing it</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2>Security practices we do claim</h2>
    <ul>
      <li>Data is held in the app's private storage area, which Android isolates from other apps.</li>
      <li>The database is excluded from Android cloud backup and from device-to-device transfer, so it is not copied into your Google account.</li>
      <li>An optional PIN plus fingerprint lock is available, verified on the device.</li>
      <li>No secret keys or API credentials are bundled in the app.</li>
    </ul>

    <h2>Security practices we do not claim</h2>
    <p>
      We would rather be accurate than reassuring. Tangent has
      <strong>not</strong> undergone an independent security audit or
      penetration test, holds no compliance certification (no SOC 2, no ISO
      27001, no HIPAA or GDPR certification &mdash; and no such certification
      exists for an app of this kind), and its local database is not separately
      encrypted beyond the protection Android gives app-private storage and
      full-device encryption. Anyone who can unlock your phone and open the app
      can read what is in it, which is why the optional app lock exists.
    </p>

    <h2>If this ever changes</h2>
    <p>
      An online feature would change these answers. If a future version adds
      one, the Google Play Data safety form and this page will both be updated
      before that version ships, and the <a href="{UP}privacy/">Privacy Policy</a>
      will say exactly what is sent and to whom.
    </p>

    <p>Questions: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  </div>
</section>
"""

DELETE = """
<section>
  <div class="wrap prose">
    <h1>Delete your data</h1>
    <p class="meta">Last updated {UPDATED} &middot; Applies to <code>{PACKAGE}</code></p>

    <div class="callout">
      <p>
        <strong>There is no account to delete.</strong> Tangent has no server
        and no user accounts, so none of your information exists anywhere
        except on your own device. That means you can erase all of it yourself,
        immediately, without asking anyone &mdash; and there is nothing we
        could delete on your behalf even if you asked.
      </p>
    </div>

    <h2>Option 1 &mdash; Erase your data, keep the app</h2>
    <p>Use this if you want a clean start without reinstalling.</p>
    <ol>
      <li>Open <strong>Settings</strong> on your Android device.</li>
      <li>Tap <strong>Apps</strong> (or <strong>Apps &amp; notifications</strong>).</li>
      <li>Find and tap <strong>Tangent</strong>.</li>
      <li>Tap <strong>Storage &amp; cache</strong> (or <strong>Storage</strong>).</li>
      <li>Tap <strong>Clear storage</strong> (or <strong>Clear data</strong>) and confirm.</li>
    </ol>
    <p>
      The app returns to a fresh install: workout history, food and water logs,
      body metrics, settings and the app-lock PIN are all gone.
    </p>

    <h2>Option 2 &mdash; Erase your data and remove the app</h2>
    <ol>
      <li>Press and hold the <strong>Tangent</strong> icon on your home screen or app drawer.</li>
      <li>Tap <strong>Uninstall</strong>, or drag it to <strong>Uninstall</strong>, and confirm.</li>
    </ol>
    <p>
      Uninstalling deletes the app's private storage, which is where all of
      your records live. Nothing is left behind and nothing is retained
      elsewhere.
    </p>

    <h2>What is deleted</h2>
    <p>Either option removes, permanently and in full:</p>
    <ul>
      <li>Your profile, display name, fitness level and goal</li>
      <li>Body metrics you entered</li>
      <li>All workout, challenge and journey progress, session history and streaks</li>
      <li>Food entries, saved custom foods, water logs and any calorie budget</li>
      <li>Fasting and breathing session history</li>
      <li>Wellness and gratitude entries</li>
      <li>All app settings, including the app-lock PIN hash</li>
    </ul>

    <div class="callout warn">
      <p>
        <strong>This cannot be undone.</strong> Because the app has no cloud
        backup, deleted history cannot be recovered &mdash; not by you and not
        by us. If you want to keep a record first, open
        <strong>Profile &rarr; Progress Dashboard</strong> and export a PDF or
        text report before you clear the data.
      </p>
    </div>

    <h2>Data retention</h2>
    <p>
      Your data is kept on your device for exactly as long as you keep the app
      installed and choose not to clear it. We hold no copy, so we apply no
      retention period.
    </p>

    <h2>Files you exported yourself</h2>
    <p>
      If you exported a progress report and shared or saved it somewhere &mdash;
      your email, a messaging app, your Downloads folder, a cloud drive &mdash;
      that copy is yours to manage. Clearing the app's data does not reach it.
    </p>

    <h2>Need help?</h2>
    <p>
      If a step above does not match your device, or you want confirmation that
      no data is held about you, email
      <a href="mailto:{EMAIL}">{EMAIL}</a> and you will get a reply. Please
      note that because there are no accounts, we cannot identify or look up an
      individual user &mdash; there is no record to look up.
    </p>
  </div>
</section>
"""


TERMS = """
<section>
  <div class="wrap prose">
    <h1>Terms of Service</h1>
    <p class="meta">Last updated {UPDATED} &middot; Applies to the Android app <code>{PACKAGE}</code></p>

    <h2>1. Agreement</h2>
    <p>
      These terms are between you and <strong>{DEVELOPER}</strong> ("we", "us"),
      the developer of Tangent Fitness &amp; Wellness ("Tangent", "the app").
      By installing or using the app you accept them. If you do not accept
      them, please uninstall the app.
    </p>

    <h2>2. Not medical advice</h2>
    <p>
      Tangent provides general fitness and wellness information. It is
      <strong>not a medical device</strong>, it does not diagnose, treat, cure
      or prevent any condition, and nothing in it is medical advice or a
      substitute for a qualified professional. The
      <a href="{UP}disclaimer/">Health &amp; Fitness Disclaimer</a> forms part of
      these terms and you should read it before exercising.
    </p>

    <h2>3. Eligibility</h2>
    <p>
      You must be at least 13 years old to use Tangent. If you are under 18,
      use it only with the agreement of a parent or guardian. The app is not
      directed at children.
    </p>

    <h2>4. Licence</h2>
    <p>
      We grant you a personal, non-exclusive, non-transferable, revocable
      licence to install and use Tangent on devices you control, for your own
      non-commercial use. We retain all rights not expressly granted.
    </p>

    <h2>5. What you may not do</h2>
    <ul>
      <li>Copy, redistribute, resell, sublicense or rent the app.</li>
      <li>Reverse engineer, decompile or disassemble it, except where that right cannot be excluded by law.</li>
      <li>Remove or obscure any copyright, trade mark or other proprietary notice.</li>
      <li>Reproduce or republish the app's exercise content, written guides or 3D assets outside the app.</li>
      <li>Use the app in any way that breaks applicable law.</li>
    </ul>

    <h2>6. Your data and your content</h2>
    <p>
      Everything you enter stays on your device; we neither receive nor store
      it. You keep ownership of it, and you are responsible for keeping your
      own copies. Because the app has no cloud backup, data lost to a cleared
      app, an uninstall, a factory reset, a lost phone or a device fault cannot
      be recovered by us. See the <a href="{UP}privacy/">Privacy Policy</a>.
    </p>

    <h2>7. Availability</h2>
    <p>
      Tangent is currently distributed through Google Play closed testing. We
      may change, suspend or discontinue the app, or any feature of it, at any
      time and without notice. We do not promise that any particular feature
      will continue to exist, and we do not guarantee uninterrupted or
      error-free operation.
    </p>

    <h2>8. Third-party terms</h2>
    <p>
      The app is distributed through Google Play, and your use of Google Play
      is governed by Google's own terms. Optional spoken coaching uses the
      text-to-speech engine installed on your device, which is provided by your
      device manufacturer or another app, under their terms. Tangent includes
      open-source components used under their respective licences; these are
      listed in the <a href="{UP}privacy/">Privacy Policy</a>.
    </p>

    <h2>9. No warranty</h2>
    <p>
      The app is provided <strong>"as is" and "as available"</strong>, without
      warranty of any kind, express or implied, including any implied warranty
      of merchantability, fitness for a particular purpose, accuracy or
      non-infringement. We do not warrant that the exercise instructions,
      calorie figures, nutritional values, timers or estimates in the app are
      accurate or suitable for you. Figures such as estimated calories burned
      and food macros are approximations from general reference data, not
      measurements of your body.
    </p>

    <h2>10. Limitation of liability</h2>
    <p>
      To the fullest extent permitted by law, we are not liable for any
      indirect, incidental, special, consequential or punitive damages, nor for
      any loss of data, profit, or goodwill, arising from your use of or
      inability to use the app. To the extent liability cannot be excluded, it
      is limited to the amount you paid for the app &mdash; which, as Tangent
      is free, is zero.
    </p>
    <p>
      Nothing in these terms excludes or limits liability for death or personal
      injury caused by our negligence, for fraud, or for any other liability
      that cannot lawfully be excluded. Some jurisdictions do not allow certain
      exclusions, so parts of this section may not apply to you.
    </p>

    <h2>11. Assumption of risk</h2>
    <p>
      Physical exercise carries inherent risk of injury. You use Tangent
      voluntarily and you accept that risk. You are responsible for deciding
      whether an exercise is appropriate for you, for exercising within your
      own limits, and for stopping when something hurts.
    </p>

    <h2>12. Changes to these terms</h2>
    <p>
      We may update these terms. The date at the top of this page will change
      when we do, and the current version is always the one published here.
      Continuing to use the app after a change means you accept the updated
      terms.
    </p>

    <h2>13. Termination</h2>
    <p>
      You may end this agreement at any time by uninstalling the app. We may
      end it if you materially breach these terms. On termination, the licence
      in section 4 ends; sections 6, 9, 10 and 11 survive.
    </p>

    <h2>14. Governing law</h2>
    <p>
      These terms are governed by the laws of the developer's place of
      residence, without regard to conflict-of-laws rules, and without
      depriving you of the protection of any mandatory consumer law of your own
      country of residence.
    </p>

    <h2>15. Contact</h2>
    <p>
      {DEVELOPER}<br>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
    </p>
  </div>
</section>
"""

DISCLAIMER = """
<section>
  <div class="wrap prose">
    <h1>Health &amp; Fitness Disclaimer</h1>
    <p class="meta">Last updated {UPDATED} &middot; Please read this before using Tangent to exercise</p>

    <div class="callout warn">
      <p>
        <strong>Tangent is not a medical device and does not give medical
        advice.</strong> It does not diagnose, treat, cure, prevent or monitor
        any disease or condition. Nothing in the app &mdash; not the workouts,
        the exercise guides, the nutrition figures, the fasting timer, the
        breathing sessions or the wellness content &mdash; is a substitute for
        advice from a doctor or another qualified health professional.
      </p>
    </div>

    <h2>Speak to a professional first</h2>
    <p>
      Consult a doctor before starting this or any exercise programme,
      particularly if any of the following applies to you:
    </p>
    <ul>
      <li>You have a heart condition, high or low blood pressure, or have been told to limit physical activity.</li>
      <li>You have chest pain, dizziness, fainting spells or shortness of breath, at rest or during exertion.</li>
      <li>You have a bone, joint, back, neck or muscle problem that exercise could aggravate.</li>
      <li>You are pregnant, recently gave birth, or are recovering from surgery, illness or injury.</li>
      <li>You have diabetes, a metabolic condition, an eating disorder, or any condition affected by fasting or changes in diet.</li>
      <li>You take medication that affects your heart rate, blood pressure, blood sugar, balance or hydration.</li>
      <li>You are over 40 and have been inactive, or you are simply unsure whether exercise is safe for you.</li>
    </ul>

    <h2>Stop if something is wrong</h2>
    <p>
      Stop exercising immediately and seek medical help if you experience chest
      pain or pressure, severe shortness of breath, dizziness, faintness,
      nausea, an irregular heartbeat, sudden or sharp pain, numbness, or any
      symptom that worries you. Discomfort from effort is normal; pain is a
      signal to stop.
    </p>

    <h2>Fasting</h2>
    <p>
      The fasting timer is a clock, not a clinical tool. Intermittent fasting
      is not appropriate for everyone &mdash; including, among others, people
      who are pregnant or breastfeeding, people with diabetes or a history of
      disordered eating, people who are underweight, children and adolescents,
      and people on certain medications. Talk to a doctor before fasting.
    </p>

    <h2>Nutrition figures are estimates</h2>
    <p>
      Calorie and macronutrient values come from a general reference catalogue
      and from any custom foods you enter yourself. Real foods vary by brand,
      portion, preparation and measurement. The figures are useful for rough
      tracking and should not be relied on for medical nutrition therapy, for
      managing a clinical condition, or by anyone who has been given a
      prescribed diet. Calories-burned figures are generic estimates, not
      measurements of your body.
    </p>

    <h2>Form and technique</h2>
    <p>
      The 3D demonstrations and written guides show a general version of each
      movement. They cannot see you, correct your form, or know your injury
      history, mobility or experience. Start light, move slowly, use the
      easier variation when one is offered, and consider working with a
      qualified trainer &mdash; especially for unfamiliar exercises.
    </p>

    <h2>Wellness and mental-health content</h2>
    <p>
      Breathing exercises, gratitude prompts, morning routines and quit
      journeys are general self-guided wellness practices. They are not
      therapy, counselling or psychiatric treatment, and they are not a crisis
      service. If you are struggling with your mental health, please contact a
      qualified professional or your local crisis line. If you are in immediate
      danger, contact your local emergency number.
    </p>

    <h2>Your responsibility</h2>
    <p>
      You use Tangent voluntarily and at your own risk. You are responsible for
      deciding which activities are suitable for you, for working within your
      own limits, and for the consequences of your training and dietary
      choices. To the extent permitted by law, {DEVELOPER} accepts no liability
      for injury, illness, loss or damage arising from your use of the app.
      See also the <a href="{UP}terms/">Terms of Service</a>.
    </p>

    <h2>Questions</h2>
    <p>
      For questions about the app itself, write to
      <a href="mailto:{EMAIL}">{EMAIL}</a>. Please note that we cannot answer
      medical questions or advise on whether a particular exercise is safe for
      you &mdash; that is a conversation for your doctor.
    </p>
  </div>
</section>
"""

SUPPORT = """
<section class="hero">
  <div class="wrap">
    <span class="eyebrow">We read every message</span>
    <h1>Contact &amp; support</h1>
    <p class="lede">
      Tangent is made by one developer. Email is the only support channel, and
      it reaches him directly.
    </p>
    <div class="actions">
      <a class="btn btn-primary" href="mailto:{EMAIL}">Email {EMAIL}</a>
    </div>
  </div>
</section>

<section>
  <div class="wrap prose">
    <h2>How to reach us</h2>
    <div class="table-scroll" role="region" aria-label="Contact details" tabindex="0">
      <table>
        <tbody>
          <tr><th scope="row">Developer</th><td>{DEVELOPER}</td></tr>
          <tr><th scope="row">Support email</th><td><a href="mailto:{EMAIL}">{EMAIL}</a></td></tr>
          <tr><th scope="row">App package</th><td><code>{PACKAGE}</code></td></tr>
          <tr><th scope="row">Platform</th><td>Android 7.0 (API 24) and newer</td></tr>
          <tr><th scope="row">Response time</th><td>Usually within a few days. This is a one-person project, not a staffed help desk.</td></tr>
        </tbody>
      </table>
    </div>

    <h2>Joining the test</h2>
    <p>
      Tangent is in closed testing on Google Play. To be added, email
      <a href="mailto:{EMAIL}">{EMAIL}</a> from &mdash; or naming &mdash; the
      Google account you use on your Android phone, since a tester invitation
      can only be sent to a Google account. You will get back a join link.
    </p>

    <h2>Reporting a problem</h2>
    <p>
      The more of this you can include, the faster it gets fixed:
    </p>
    <ul>
      <li>What you were doing, and what happened instead of what you expected.</li>
      <li>The screen it happened on.</li>
      <li>Your device model and Android version (<strong>Settings &rarr; About phone</strong>).</li>
      <li>The app version (<strong>Profile</strong> screen, or the Play Store listing).</li>
      <li>A screenshot, if the problem is visible.</li>
    </ul>
    <div class="callout">
      <p>
        <strong>If the app crashed:</strong> reopen it. Tangent saves a
        technical report of the previous crash and shows it to you on the next
        launch. Screenshot that screen and attach it &mdash; it names the exact
        line that failed. That report is stored only on your device and is
        never sent anywhere automatically.
      </p>
    </div>

    <h2>Common questions</h2>

    <h3>Do I need an account?</h3>
    <p>
      No. There is no sign-up, and there is nothing to log in to. Open the app
      and start.
    </p>

    <h3>Does Tangent work without internet?</h3>
    <p>
      Yes &mdash; entirely. The app has no internet permission and no
      networking code, so every feature works offline by design. There is
      nothing that needs a connection.
    </p>

    <h3>Will my data sync to a new phone?</h3>
    <p>
      No. Your records live only on the device that created them, and the
      database is deliberately excluded from Android backup and device
      transfer. Before switching phones, export a progress report from
      <strong>Profile &rarr; Progress Dashboard</strong> to keep a copy of your
      history.
    </p>

    <h3>I forgot my app-lock PIN.</h3>
    <p>
      The PIN is stored only as a salted hash on your device, so it cannot be
      recovered or reset by us &mdash; there is no account behind it. If you
      cannot get in, clearing the app's data removes the lock, but it also
      erases your history. See <a href="{UP}delete-data/">Delete your data</a>.
    </p>

    <h3>Why don't my reminders arrive exactly on time?</h3>
    <p>
      Reminders are scheduled inexactly on purpose, so Android can batch them
      and save battery, and the app does not ask for exact-alarm permission.
      Expect a few minutes' variance. Battery-saver and app-standby settings on
      your device can delay them further.
    </p>

    <h3>Can I scan barcodes or photograph my food?</h3>
    <p>
      No. Both would require sending data to a server, and Tangent has no
      network access. You can search the built-in food catalogue or save your
      own custom foods with their values.
    </p>

    <h3>How do I delete everything?</h3>
    <p>
      Uninstall the app, or clear its data in Android settings. Full steps are
      on <a href="{UP}delete-data/">Delete your data</a>.
    </p>

    <h3>Is Tangent free?</h3>
    <p>
      Yes. There are no ads, no in-app purchases and no subscription.
    </p>

    <h2>Also worth reading</h2>
    <ul>
      <li><a href="{UP}privacy/">Privacy Policy</a> &mdash; what is stored, and what is not</li>
      <li><a href="{UP}data-safety/">Data Safety</a> &mdash; the Google Play declaration, explained</li>
      <li><a href="{UP}disclaimer/">Health &amp; Fitness Disclaimer</a> &mdash; read before exercising</li>
      <li><a href="{UP}terms/">Terms of Service</a></li>
    </ul>
  </div>
</section>
"""


NOT_FOUND = """
<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Error 404</span>
    <h1>That page isn't here</h1>
    <p class="lede">
      The link may be out of date. Everything on this site is reachable from
      the navigation above.
    </p>
    <div class="actions">
      <a class="btn btn-primary" href="./">Go to the home page</a>
      <a class="btn btn-ghost" href="{UP}support/">Contact support</a>
    </div>
  </div>
</section>
"""

JSONLD_HOME = """<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Tangent Fitness & Wellness",
  "operatingSystem": "Android 7.0+",
  "applicationCategory": "HealthApplication",
  "applicationSubCategory": "Fitness",
  "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "USD" }},
  "author": {{ "@type": "Person", "name": "{DEVELOPER}" }},
  "publisher": {{ "@type": "Person", "name": "{DEVELOPER}" }},
  "url": "{BASE_URL}/",
  "description": "Offline-first fitness and wellness app for Android: workout challenges, a 3D exercise library, a written guide to 500 exercises, nutrition and water logging, fasting and breathing timers, and progress tracking. No account, no ads, no data collection.",
  "isAccessibleForFree": true,
  "privacyPolicy": "{BASE_URL}/privacy/"
}}
</script>
"""

# slug, <title>, meta description, body, extra head
PAGES = [
    ("", "Tangent Fitness & Wellness — Offline Android fitness app",
     "Tangent is an offline-first Android fitness and wellness app: workout challenges, a 3D exercise library, 500 written exercise guides, nutrition logging, fasting and breathing timers. No account, no ads, no data collection.",
     HOME, JSONLD_HOME),
    ("privacy/", "Privacy Policy — Tangent Fitness & Wellness",
     "Tangent collects no data. It has no internet permission, no accounts, no analytics and no ads. Everything you enter stays in the app's private storage on your device.",
     PRIVACY, ""),
    ("data-safety/", "Data Safety — Tangent Fitness & Wellness",
     "The Google Play Data safety declaration for Tangent, explained: no data collected, no data shared, and exactly what the app stores on your device.",
     DATA_SAFETY, ""),
    ("terms/", "Terms of Service — Tangent Fitness & Wellness",
     "Terms of Service for the Tangent Fitness & Wellness Android app, including licence, warranty, assumption of risk and limitation of liability.",
     TERMS, ""),
    ("disclaimer/", "Health & Fitness Disclaimer — Tangent Fitness & Wellness",
     "Tangent is not a medical device and does not give medical advice. Read this before starting any exercise programme, fasting, or relying on nutrition figures.",
     DISCLAIMER, ""),
    ("delete-data/", "Delete your data — Tangent Fitness & Wellness",
     "How to permanently erase all Tangent data. There is no account to delete: everything is on your device, and clearing app data or uninstalling removes it.",
     DELETE, ""),
    ("support/", "Contact & Support — Tangent Fitness & Wellness",
     "Contact the developer of Tangent Fitness & Wellness. Support email, how to join the closed test, how to report a problem, and answers to common questions.",
     SUPPORT, ""),
]

SUBS = {
    "EMAIL": EMAIL,
    "DEVELOPER": DEVELOPER,
    "PACKAGE": PACKAGE,
    "UPDATED": UPDATED,
    "BASE_URL": BASE_URL,
}


def fill(text: str, slug: str = "") -> str:
    """
    Substitutes the shared values, plus {UP} — the number of `../` hops back to
    the site root from this page.

    Body links go through {UP} because they are relative: `delete-data/`
    written on /privacy/ resolves to /privacy/delete-data/, which is a dead
    link. Relative paths are what let the same files serve correctly both at a
    domain root and under a GitHub Pages repository subpath, so the fix is to
    make the depth explicit rather than to switch to absolute paths.
    """
    up = "../" * (slug.count("/") if slug else 0)
    return text.format(UP=up, **SUBS)


def main() -> None:
    written = []
    for slug, title, desc, body, head in PAGES:
        out = ROOT / slug / "index.html" if slug else ROOT / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            shell(slug, title, desc, fill(body, slug), fill(head, slug) if head else "")
        )
        written.append(str(out.relative_to(ROOT)))

    # 404.html sits at the root and is served by GitHub Pages for unknown paths.
    (ROOT / "404.html").write_text(
        shell("", "Page not found — Tangent Fitness & Wellness",
              "That page could not be found.", fill(NOT_FOUND))
    )
    written.append("404.html")

    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n"
    )
    written.append("robots.txt")

    urls = "\n".join(
        "  <url><loc>{base}/{slug}</loc><changefreq>monthly</changefreq>"
        "<priority>{pri}</priority></url>".format(
            base=BASE_URL, slug=slug, pri="1.0" if slug == "" else "0.8"
        )
        for slug, *_ in PAGES
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n"
    )
    written.append("sitemap.xml")

    # Tells GitHub Pages to serve the files as-is instead of running Jekyll,
    # which would otherwise ignore any directory beginning with an underscore.
    (ROOT / ".nojekyll").write_text("")
    written.append(".nojekyll")

    print(f"built {len(written)} files:")
    for w in written:
        print("  " + w)


if __name__ == "__main__":
    main()
