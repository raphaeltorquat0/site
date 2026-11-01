# Decisões

| # | Decisão | Motivo |
|---|---|---|
| 1 | HTML/CSS gerado por `build.py`, sem Astro | Três páginas e nenhuma dependência para manter. |
| 2 | Changelog no build, não no navegador | O navegador de quem visita não fala com a API do GitHub, e não há limite de 60 requisições por hora por IP. |
| 3 | Falha da API derruba o build, exceto 404 | Melhor manter o deploy anterior do que publicar sem changelog. 404 significa repositório ainda não público. |
| 4 | Build diário por cron | Pega releases novos sem acoplar o workflow de release ao site. |
| 5 | Fontes do sistema | Público no Mac, e nenhuma fonte externa é carregada. |
| 6 | A "quietisland" preta no topo é a navegação | É o elemento marcante e a única peça de interface que se move, uma vez, no carregamento. Respeita `prefers-reduced-motion`. Os vídeos de demonstração são conteúdo (#10). |
| 7 | Screenshots só do Quietbar | São as únicas capturas reais encontradas. A seção some enquanto a lista estiver vazia. As imagens em `images/` do Quietbar são de modelo 3D de terceiros e não foram usadas. |
| 8 | Quietbar, não SonyCtl | Nome atual do app. A marca Sony aparece só para descrever compatibilidade, com aviso de não afiliação. |
| 9 | Texto de privacidade reflete o estado atual de cada app | Ao mudar o que um app coleta ou acessa, atualize `apps.json`. O Quietbar usa Sparkle. |
| 10 | Vídeo da automação sem JavaScript | Um `<video>` por tema e formato, e o CSS mostra um: `poster` não aceita media query. Todo `<source>` exige `prefers-reduced-motion: no-preference`, então com movimento reduzido nada é baixado e fica o pôster. Custo: as quatro tags pedem o próprio pôster. |
| 11 | Só em inglês | O site é todo em inglês. Os vídeos e pôsteres em português ficam em `assets/quietbar/automation` para posts. |
| 12 | Prévia local com `python3 -m http.server` | O site não tem servidor de desenvolvimento. Esse comando não atende `Range`, que o Safari costuma exigir para vídeo; o GitHub Pages atende. |
| 13 | WebM primeiro, MP4 como fallback, sem prova no Safari real | O WebKit do Playwright tocou o WebM em todos os formatos. Com só o MP4 ele carrega, mas não inicia sozinho, com ou sem `preload` e `media`; `play()` funciona. Pior caso para um Safari sem VP9: o pôster parado. Falta conferir num iPhone. |
