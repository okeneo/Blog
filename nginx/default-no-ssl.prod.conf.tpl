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
        return 301 http://${DOMAIN}$request_uri;
    }
}

server {
    listen 80;
    server_name ${DOMAIN};
    server_tokens off;

    client_max_body_size 10M;

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
        proxy_set_header X-Forwarded-Proto http;
        proxy_set_header X-Url-Scheme $scheme;
    }

    location /django-static/ {
        alias /staticfiles/;
    }
}
