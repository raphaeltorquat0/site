# Site

Static site for the portfolio. Python standard library only, no framework, no analytics, and no requests to third parties from the visitor's browser.

[Versão em português](README.pt-BR.md)

```sh
python3 build.py        # writes dist/
python3 -m http.server 8765 --directory dist   # videos need a server, not file://
```

Apps live in `apps.json`, images in `assets/<slug>/`. Changelogs are read from GitHub Releases at build time. The site rebuilds on every push and once a day.

## License

MIT. See [LICENSE](LICENSE).
