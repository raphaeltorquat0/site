#!/usr/bin/env python3
"""Builds the static site into dist/. Standard library only.

Changelogs come from the GitHub API at build time, so visitors' browsers never call a third
party. Run with GITHUB_TOKEN set to avoid the anonymous rate limit.
"""
import html
import json
import os
import re
import shutil
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
ORG = "raphaeltorquat0"
BMC = "https://buymeacoffee.com/raphaeltorquato"
DOMAIN = "raphaeltorquat0.github.io/site"


def fetch_releases(repo):
    request = urllib.request.Request(
        f"https://api.github.com/repos/{ORG}/{repo}/releases?per_page=20",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "portfolio-site"},
    )
    if token := os.environ.get("GITHUB_TOKEN"):
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            releases = json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:  # Not published yet. Any other failure must stop the deploy.
            return []
        raise
    return [r for r in releases if not r["draft"]]


def inline(text):
    text = html.escape(text, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def markdown(body):
    """Covers what release-notes.py writes. Anything else stays visible as plain text."""
    out, in_list = [], False
    for line in (body or "").splitlines():
        if line.startswith("- "):
            if not in_list:
                out.append("<ul>")
            out.append(f"<li>{inline(line[2:])}</li>")
            in_list = True
            continue
        if in_list:
            out.append("</ul>")
            in_list = False
        if line.startswith("#"):
            out.append(f"<h3>{inline(line.lstrip('# '))}</h3>")
        elif line.strip() and not line.startswith(">"):
            out.append(f"<p>{inline(line)}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def changelog(releases, repo):
    if not releases:
        return f'<p>No releases yet. <a href="https://github.com/{ORG}/{repo}">Watch the repository</a> to hear about the first one.</p>'
    items = []
    for index, release in enumerate(releases):
        title = html.escape(release["name"] or release["tag_name"])
        date = release["published_at"][:10]
        tag = " (beta)" if release["prerelease"] else ""
        items.append(
            f'<details{" open" if index == 0 else ""}><summary>{title}{tag}<time datetime="{date}">{date}</time></summary>'
            f'{markdown(release["body"])}</details>'
        )
    return "\n".join(items)


def page(title, description, body, depth, current=None, apps=()):
    prefix = "../" * depth
    links = [f'<a href="{prefix}index.html"{" aria-current=\"page\"" if current == "home" else ""}>All apps</a>']
    for app in apps:
        attr = ' aria-current="page"' if current == app["slug"] else ""
        links.append(
            f'<a href="{prefix}{app["slug"]}/index.html"{attr}>'
            f'<img src="{prefix}assets/{app["slug"]}/icon.png" alt="">{app["name"]}</a>'
        )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="icon" href="{prefix}assets/quietbar/icon.png">
<link rel="stylesheet" href="{prefix}style.css">
</head>
<body>
<nav class="island" aria-label="Apps">{''.join(links)}</nav>
<main>
{body}
</main>
<footer>
<a href="{BMC}">Buy Me a Coffee</a>
<a href="https://github.com/{ORG}">GitHub</a>
<p>This site has no analytics and sets no cookies.</p>
</footer>
</body>
</html>
"""


def home(apps):
    rows = "\n".join(
        f"""<section class="app {a['color']}">
<h2><a href="{a['slug']}/index.html">{a['name']}</a></h2>
<p>{html.escape(a['tagline'])}</p>
</section>"""
        for a in apps
    )
    body = f"""<div class="intro">
<h1>Small, native apps for the Mac</h1>
<p>Free and open source, with every feature included. Paid for by people who choose to chip in.</p>
</div>
{rows}"""
    return page("Mac apps", "Free, open source, native apps for the Mac.", body, 0, "home", apps)


def demo_section(app):
    """One <video> per theme and shape, and CSS shows one: a poster can't depend on a media query.

    Every <source> needs prefers-reduced-motion: no-preference, so with reduced motion nothing
    matches, no video is requested, and the poster stays.
    """
    demo = app.get("demo")
    if not demo:
        return ""
    base = f'../assets/{app["slug"]}/{demo["folder"]}/automation'
    alt = html.escape(demo["alt"])
    videos = []
    for name, width, height, shape in (("16x10", 1600, 1000, "(min-width: 601px)"), ("9x16", 1080, 1920, "(max-width: 600px)")):
        for theme in ("light", "dark"):
            media = f"(prefers-reduced-motion: no-preference) and {shape} and (prefers-color-scheme: {theme})"
            sources = "".join(
                f'<source src="{base}-{name}-{theme}-en.{kind}" type="video/{kind}" media="{media}">' for kind in ("webm", "mp4")
            )
            videos.append(
                f'<video class="demo-{name} demo-{theme}" autoplay muted loop playsinline preload="metadata" '
                f'width="{width}" height="{height}" poster="{base}-{name}-{theme}-en.webp" aria-label="{alt}">{sources}</video>'
            )
    upcoming = '<p class="upcoming">Coming in the next version</p>\n' if demo.get("upcoming") else ""
    return f"""<h2>{html.escape(demo["heading"])}</h2>
{upcoming}<p>{html.escape(demo["text"])}</p>
<div class="demo">{''.join(videos)}</div>
"""


def app_page(app, releases):
    slug, repo = app["slug"], app["repo"]
    shots = "".join(
        f'<img src="../assets/{slug}/{s["file"]}" alt="{html.escape(s["alt"])}" loading="lazy">'
        for s in app["screenshots"]
    )
    shots_section = f'<h2>Screenshots</h2><div class="shots">{shots}</div>' if shots else ""
    requirements = "".join(f"<li>{html.escape(r)}</li>" for r in app["requirements"])
    body = f"""<article class="page {app['color']}">
<header>
<img src="../assets/{slug}/icon.png" alt="">
<h1>{app['name']}</h1>
</header>
<p class="lede">{html.escape(app['tagline'])}</p>
<p>{html.escape(app['description'])}</p>
<p><a class="button" href="https://github.com/{ORG}/{repo}/releases/latest">Download {app['name']}</a></p>
{demo_section(app)}{shots_section}
<h2>Requirements</h2>
<ul>{requirements}</ul>
<h2>Install with Homebrew</h2>
<pre><code>brew install --cask {ORG}/tap/{slug}</code></pre>
<h2>Changelog</h2>
{changelog(releases, repo)}
<h2>Privacy</h2>
<p>{html.escape(app['privacy'])}</p>
<h2>Support {app['name']}</h2>
<p>Every feature is free. If the app helps you, <a href="{BMC}">buy me a coffee</a>.</p>
<p><a href="https://github.com/{ORG}/{repo}">Source code</a> and <a href="https://github.com/{ORG}/{repo}/issues">issues</a> are on GitHub.</p>
</article>"""
    return page(f"{app['name']} for Mac", app["tagline"], body, 1, slug, APPS)


APPS = [a for a in json.loads((ROOT / "apps.json").read_text()) if not a.get("hidden")]


def main():
    shutil.rmtree(DIST, ignore_errors=True)
    DIST.mkdir()
    shutil.copytree(ROOT / "assets", DIST / "assets")
    shutil.copy(ROOT / "style.css", DIST)
    (DIST / ".nojekyll").touch()
    if "/" not in DOMAIN and not DOMAIN.endswith(".github.io"):
        (DIST / "CNAME").write_text(DOMAIN + "\n")
    (DIST / "index.html").write_text(home(APPS))
    for app in APPS:
        directory = DIST / app["slug"]
        directory.mkdir()
        (directory / "index.html").write_text(app_page(app, fetch_releases(app["repo"])))


if __name__ == "__main__":
    main()
