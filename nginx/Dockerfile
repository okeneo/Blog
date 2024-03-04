FROM nginx:1.25.4-alpine

COPY . /etc/nginx

ENV API_HOST=api
ENV API_PORT=8000

RUN apk add --no-cache openssl bash
RUN chmod +x /etc/nginx/run.sh

CMD ["/etc/nginx/run.sh"]
