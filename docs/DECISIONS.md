# Decisões

| # | Decisão | Motivo |
|---|---|---|
| 1 | HTML/CSS gerado por `build.py`, sem Astro | Três páginas e nenhuma dependência para manter. |
| 2 | Changelog no build, não no navegador | O navegador de quem visita não fala com a API do GitHub, e não há limite de 60 requisições por hora por IP. |
| 3 | Falha da API derruba o build, exceto 404 | Melhor manter o deploy anterior do que publicar sem changelog. 404 significa repositório ainda não público. |
| 4 | Build diário por cron | Pega releases novos sem acoplar o workflow de release ao site. |
| 5 | Fontes do sistema | Público no Mac, e nenhuma fonte externa é carregada. |
| 6 | A "ilha" preta no topo é a navegação | É o elemento marcante e o único que se move, uma vez, no carregamento. Respeita `prefers-reduced-motion`. |
| 7 | Screenshots só do Quietbar | São as únicas capturas reais encontradas. A seção some enquanto a lista estiver vazia. As imagens em `images/` do Quietbar são de modelo 3D de terceiros e não foram usadas. |
| 8 | Quietbar, não SonyCtl | Nome atual do app. A marca Sony aparece só para descrever compatibilidade, com aviso de não afiliação. |
| 9 | Texto de privacidade reflete o estado atual de cada app | Quietbar e DungeonDrafter não têm updater hoje. Ao ligar o Sparkle neles, atualize `apps.json`. |
