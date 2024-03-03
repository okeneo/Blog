#!/bin/bash

set -e

echo "Checking for dhparams.pem..."
if [ ! -f "/etc/letsencrypt/ssl-dhparams.pem" ]; then
    echo "dhparams.pem does not exist - creating it"
    openssl dhparam -out /etc/letsencrypt/ssl-dhparams.pem 2048
fi

# Avoid replacing these with envsubst.
export host=\$host
export request_uri=\$request_uri
export uri=\$uri
export proxy_add_x_forwarded_for=\$proxy_add_x_forwarded_for
export scheme=\$scheme

echo "Checking for fullchain.pem"
echo "/etc/letsencrypt/live/$DOMAIN/fullchain.pem"
if [ ! -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    echo "No SSL certificate. Enabling HTTP only..."
    envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
else
    echo "SSL certificate exists. Enabling HTTPS..."
    envsubst < /etc/nginx/default-ssl.conf.tpl > /etc/nginx/conf.d/default.conf
fi

nginx -g "daemon off;"
