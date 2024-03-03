#!/bin/sh

# Waits for the proxy to be available, then gets the first certificate.

set -e

check_nginx() {
    ping -c 1 nginx
}

until check_nginx; do
    echo "Waiting for proxy..."
    sleep 5s & wait ${!}
done

echo "Getting certificate..."

certbot certonly \
    --webroot \
    --webroor-path "/var/www/certbot" \
    -d "$DOMAIN" \
    --email "$ACME_DEFAULT_EMAIL" \
    --rsa-key-size 4096 \
    --agree-tos \
    -noninteractive
