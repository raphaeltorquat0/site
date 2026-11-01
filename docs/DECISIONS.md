# Decisões

| # | Decisão | Motivo |
|---|---|---|
| 1 | HTML/CSS gerado por `build.py`, sem Astro | Três páginas e nenhuma dependência para manter. |
| 2 | Changelog no build, não no navegador | O navegador de quem visita não fala com a API do GitHub, e não há limite de 60 requisições por hora por IP. |
| 3 | Falha da API derruba o build, exceto 404 | Melhor manter o deploy anterior do que publicar sem changelog. 404 significa repositório ainda não público. |
| 4 | Build diário por cron | Pega releases novos sem acoplar o workflow de release ao site. O GitHub desliga o cron depois de 60 dias sem atividade no repositório; um push ou reativar o workflow religa. |
| 5 | Fontes do sistema | Público no Mac, e nenhuma fonte externa é carregada. |
| 6 | A "quietisland" preta no topo é a navegação | É o elemento marcante e a única peça de interface que se move, uma vez, no carregamento. Respeita `prefers-reduced-motion`. Os vídeos de demonstração são conteúdo (#10). |
| 7 | Screenshots só do Quietbar | São as únicas capturas reais encontradas. A seção some enquanto a lista estiver vazia. As imagens em `images/` do Quietbar são de modelo 3D de terceiros e não foram usadas. |
| 8 | Quietbar, não SonyCtl | Nome atual do app. A marca Sony aparece só para descrever compatibilidade, com aviso de não afiliação. |
| 9 | Texto de privacidade reflete o estado atual de cada app | O texto descreve a versão publicada, não a `main` do app. Ao publicar uma versão que muda o que um app coleta ou acessa, atualize `apps.json`. O Quietbar usa Sparkle. |
| 10 | Vídeo da automação sem JavaScript | Um `<video>` por tema e formato, e o CSS mostra um: `poster` não aceita media query. Todo `<source>` exige `prefers-reduced-motion: no-preference`, então com movimento reduzido nada é baixado e fica o pôster. Custo: as quatro tags pedem o próprio pôster. |
| 11 | Só em inglês | O site é todo em inglês. Os vídeos e pôsteres em português ficam em `assets/quietbar/automation` para posts. |
| 12 | Prévia local com `python3 -m http.server` | O site não tem servidor de desenvolvimento. Esse comando não atende `Range`, que o Safari costuma exigir para vídeo; o GitHub Pages atende. |
| 13 | WebM primeiro, MP4 como fallback, sem prova no Safari real | O WebKit do Playwright tocou o WebM em todos os formatos. Com só o MP4 ele carrega, mas não inicia sozinho, com ou sem `preload` e `media`; `play()` funciona. Pior caso para um Safari sem VP9: o pôster parado. Falta conferir num iPhone. |
| 14 | Sem GitHub Sponsors | A conta não tem perfil de Sponsors (`hasSponsorsListing: false`, 1/11/2026), e o link levaria para o perfil comum. Fica só o Buy Me a Coffee. Volte com o link quando o perfil estiver ativo. |
| 15 | Flag `hidden` em `apps.json` | Esconde o app da navegação, da home e das páginas, para não gerar link 404. Em 1/11/2026 o repositório do QuietIsland não existe e o do DungeonDrafter é privado. Retire a flag quando o repositório for público. |
| 16 | `demo.upcoming` em `apps.json` | Mostra "Coming in the next version" na seção de automação, que descreve a 1.4.0. Retire a flag ao publicar a 1.4.0. |
| 17 | Links relativos | O site roda em `/site/`. Todo link interno e asset usa caminho relativo à página, então nada depende do subcaminho. |
| 18 | Build exige Python 3.12+ | `build.py` usa barra invertida dentro de f-string. O `ubuntu-latest` já traz essa versão, sem `setup-python`. |
| 19 | Ambiente `github-pages` aceita `main` | O ambiente foi criado permitindo só a branch `release`, e o deploy era recusado antes do primeiro passo. A regra de `main` foi adicionada à política do ambiente. |
