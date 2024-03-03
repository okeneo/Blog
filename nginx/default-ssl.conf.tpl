upstream myproject {
    server ${API_HOST}:${API_PORT};
}

server {
    listen 80;
    server_name ${DOMAIN} www.${DOMAIN};
    server_tokens off;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name ${DOMAIN} www.${DOMAIN};
    server_tokens off;

    ssl_certificate /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;
    include /etc/nginx/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    client_max_body_size 20M;

    location / {
        alias /var/www/frontend/;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        try_files $uri @proxy_api;
    }

    location @proxy_api {
        proxy_pass http://myproject;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Url-Scheme $scheme;
    }

    location /django-static/ {
        alias /staticfiles/;
    }

}
