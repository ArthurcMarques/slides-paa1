# Apresentação: Shell Sort e Selection Sort

Abra `Shell_e_Selection_Sort.html` no navegador. O arquivo é completo e funciona sem internet.

## Pastas

- `dados/`: os três CSVs originais do Shell Sort.
- `scripts/`: script para gerar a apresentação completa.
- `build/shell/`: imagens dos slides Shell, manifesto, verificação de JavaScript e prévia visual.
- `historico/selection-sort/`: versão anterior de Selection Sort, usada como base e preservada com seus arquivos de projeto.
- `distribuicao/`: pacotes ZIP para compartilhar.
- `site/`: site estático pronto para o Nginx, com `index.html`.

## Gerar novamente

Na raiz do projeto, execute:

```powershell
python scripts/build_shell_selection.py
```

Requer Python, Pillow e as fontes DejaVu Sans. O caminho das fontes está definido em `FONT` no script.

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
- URL do serviço: `IP_DO_HOMELAB:8080` (use um IP da rede local alcançável pelo container Cloudflared).

Como o Cloudflared está em outro container, `localhost:8080` aponta para o próprio Cloudflared. Use o IP do host nesse modelo. O túnel oferece o acesso HTTPS pelo domínio; a página é servida em HTTP dentro da rede.

Nesse modelo, o Cloudflared encaminha diretamente para a página na porta 8080. A configuração atual serve HTTP; o HTTPS público fica a cargo do Cloudflare Tunnel.

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
