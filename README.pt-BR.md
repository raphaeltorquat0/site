# Site

Site estático do portfólio. Só biblioteca padrão do Python, sem framework, sem analytics e sem requisições a terceiros a partir do navegador de quem visita.

[English version](README.md)

```sh
python3 build.py        # gera dist/
open dist/index.html
```

Os apps ficam em `apps.json`, as imagens em `assets/<slug>/`. O changelog vem dos GitHub Releases na hora do build. O site é refeito a cada push e uma vez por dia.

## Licença

MIT. Veja [LICENSE](LICENSE).
