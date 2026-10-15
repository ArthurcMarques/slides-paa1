FROM nginx:stable-alpine

COPY --chmod=644 docker/default.conf /etc/nginx/conf.d/default.conf
COPY site/ /usr/share/nginx/html/

# Arquivos vindos de pastas compartilhadas podem chegar sem leitura para o nginx.
RUN chmod -R a+rX /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=10s --timeout=10s --start-period=15s --retries=3 \
    CMD wget -T 8 -O /dev/null http://127.0.0.1/index.html || exit 1
