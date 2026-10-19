# Apresentação: Shell Sort e Selection Sort

Abra `Shell_e_Selection_Sort.html` no navegador. O arquivo é completo e funciona sem internet.

No celular, a navegação se organiza em linhas e as animações exibem vetor e código em uma coluna, com rolagem vertical. Use **Ampliar** para ler slides estáticos arrastando na horizontal e **Ajustar** para voltar à visão completa. Deslizar lateralmente troca de slide quando a ampliação está desativada; os controles das animações continuam independentes.

Use o botão **Slides** (ou a tecla **M**, inclusive em tela cheia) para ocultar slides. Desmarque os que devem ser pulados; “Exibir todos” os restaura. Botões, teclado e gestos navegam apenas pelos visíveis. A seleção fica salva no navegador quando o armazenamento local está disponível e é independente para cada slide da apresentação e do apoio. Sempre permanece pelo menos um slide visível por parte. Os PDFs continuam completos, sem aplicar essa preferência local.

A sequência principal tem **30 slides**: capa, Shell, Selection, computador, comparação e conclusão, com dois slides de bibliografia, um para cada algoritmo, no final. Além das animações de Shell e Selection, há um slide extra de Shell por subsequências e um resumo sobre a dificuldade da análise matemática. O botão **Material de apoio** abre 33 slides adicionais com tabelas, gráficos de contagens e explicações completas; “Voltar à apresentação” retorna à sequência principal. Todo o conteúdo está incorporado no mesmo HTML.

O PDF principal contém os 27 slides. `output/pdf/Shell_e_Selection_Sort_Apoio.pdf` contém o apoio completo. Para exportar novamente, execute `python scripts/export_pdf.py` e `python scripts/export_pdf.py --apoio` (requer ReportLab e PyMuPDF). Mantenha os dois PDFs na mesma pasta para os links entre eles funcionarem.

O exemplo de Shell é uma animação interativa com vetor, código em C e linha ativa. Há reprodução, pausa, passos para frente e para trás, reinício, velocidade e atalhos para gaps 4, 2 e 1. `scripts/shell-animation.js` gera os estados da execução; o CSS fica em `scripts/shell-animation.css`. O PDF mostra um resumo estático com o código, pois não executa animações.
Selection também tem uma animação com os mesmos controles, índices i/j/menor, ordem da busca, parte ordenada, troca e contadores de comparações e escritas. Ela substitui a sequência antiga de exemplos estáticos. Os arquivos são `scripts/selection-animation.js` e `scripts/selection-animation.css`.

## Pastas

- `dados/`: os três CSVs originais do Shell Sort.
- `scripts/`: script para gerar a apresentação completa.
- `build/shell/`: imagens dos slides Shell, manifesto, verificação de JavaScript e prévia visual.
- `historico/selection-sort/`: versão anterior de Selection Sort, usada como base e preservada com seus arquivos de projeto.
- `distribuicao/`: pacotes ZIP para compartilhar.
- `site/`: site estático pronto para o Nginx, com `index.html`.
- `graficos/referencia/`: gráficos fornecidos para orientar os slides de resultados.

## Gerar novamente

Na raiz do projeto, execute:

```powershell
python scripts/build_shell_selection.py
```

Requer Python, Pillow, Matplotlib e as fontes DejaVu Sans. O caminho das fontes está definido em `FONT` no script.

Os nove slides de resultados de Shell substituem as tabelas por gráficos, nesta ordem: três de tempo, três de comparações e três de movimentações. Cada bloco mostra entrada aleatória, crescente e decrescente, comparando Metades, Knuth e Ciura fixo. Os gráficos usam os CSVs originais, com escalas logarítmicas e o estilo visual da apresentação.
Cada gráfico é seguido por uma tabela com os valores exatos. Também há tabelas após os três gráficos de comparação de tempos entre Selection e Shell por metades.

Na parte de Shell, há um slide de vantagens e desvantagens e, após os gráficos, a conclusão sobre a escolha dos gaps. Após Selection, seis slides apresentam a comparação com Shell por metades e a conclusão dos dois algoritmos. Os dados e o texto vêm das seções 4 e 7 de `Trabalho_PAA1 (2).pdf` (páginas impressas 27–33). `dados/selection_tempos_relatorio.csv` transcreve os 30 tempos de Selection dessas tabelas. A comparação não inclui Knuth nem Ciura. A bibliografia permanece no final.

## Hospedar no Nginx existente

Publique o conteúdo de `site/` na pasta servida pelo Nginx para `paa1.arthurcmarques.com.br`. Também pode extrair `distribuicao/site.zip` nessa pasta: o pacote contém apenas `index.html`, sem pastas adicionais.

O HTML já inclui imagens, estilos e JavaScript. Não precisa de outro container nem de instalar dependências no servidor.

Se a pasta do servidor for `/srv/slides`, por exemplo, monte-a no container Nginx existente:

```yaml
volumes:
  - /srv/slides:/usr/share/nginx/slides:ro
```

No bloco do domínio, configure `root /usr/share/nginx/slides;` e `index index.html;`. Mantenha a configuração de HTTPS do seu Nginx.

Ao gerar novamente a apresentação, `site/index.html` e `distribuicao/site.zip` também são atualizados.

## Container da página sem proxy

O Compose inicia apenas `slides`: o Nginx interno serve o conteúdo de `site/` diretamente na porta 8080 do homelab, sem um container de proxy separado.

1. Se quiser alterar a porta ou o endereço de escuta, copie `.env.example` para `.env` e ajuste os valores.
2. Na raiz do projeto, execute:

```sh
docker compose up -d --build --remove-orphans
```

3. Abra `http://IP_DO_HOMELAB:8080` em outro computador da rede ou `http://localhost:8080` no próprio servidor.

A porta pode ser alterada com `SLIDES_PORT` no `.env` (exemplo: `SLIDES_PORT=80`). O endereço de escuta é definido por `SLIDES_BIND_ADDRESS`. Se houver variáveis antigas `PROXY_PORT` e `PROXY_BIND_ADDRESS` no `.env`, substitua-as pelas novas. A porta 8080 indicada como `8080/tcp` pelo cAdvisor é interna ao container; isso não ocupa a porta 8080 do host.

Na primeira atualização, `--remove-orphans` remove o antigo serviço `proxy` deste projeto. Os containers de outros projetos, como o Cloudflared, não são alterados.

### Domínio com Cloudflare Tunnel (opcional)

Se o Cloudflared existente é o túnel usado para publicar seus serviços, adicione uma rota de aplicação publicada no túnel:

- Hostname: `paa1.arthurcmarques.com.br`.
- Tipo do serviço: `HTTP`.
- URL do serviço: `http://slides:80`.

O Compose conecta a página à rede externa `homelab`, já usada pelo Cloudflared. Essa rede deve existir no servidor. Assim, o Tunnel encontra o serviço pelo nome `slides`, sem usar o IP local. `localhost` dentro do Cloudflared aponta para o próprio container.

Nesse modelo, o Cloudflared encaminha diretamente para a página na porta interna 80. A porta 8080 do host continua disponível para testes na rede local. A configuração atual serve HTTP; o HTTPS público fica a cargo do Cloudflare Tunnel.

Para publicação direta na Internet sem túnel, configure o DNS, as portas do roteador e um certificado TLS no servidor HTTP; essa configuração não está incluída.

Depois de atualizar `site/index.html`, execute novamente `docker compose up -d --build`.

```sh
docker compose ps
docker compose logs -f slides
docker compose down
```

### Se o container aparecer como unhealthy

O Dockerfile garante leitura dos arquivos estáticos pelo Nginx, inclusive quando o projeto vem de uma pasta compartilhada. O healthcheck verifica o próprio `index.html` e guarda os erros no diagnóstico do Docker.

Depois de atualizar os arquivos, reconstrua e confira:

```sh
docker compose up -d --build --force-recreate
docker compose ps
docker compose logs --tail=50 slides
docker compose exec slides wget -S -O /dev/null http://127.0.0.1/index.html
```

Para consultar a saída do healthcheck, use o nome do container mostrado em `docker compose ps`:

```sh
docker inspect --format '{{json .State.Health}}' apresentao-slides-1
```
