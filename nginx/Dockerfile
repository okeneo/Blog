FROM nginx:1.25.4-alpine

# COPY default.conf /etc/nginx/conf.d/default.conf
COPY . /etc/nginx

ENV API_HOST=api
ENV API_PORT=8000

RUN apk add --no-cache openssl bash
RUN chmod +x /etc/nginx/run.sh

VOLUME /var/www/

CMD ["/etc/nginx/run.sh"]
