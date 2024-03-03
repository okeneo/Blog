#!/bin/sh

# Waits for the proxy to be available, then gets the first certificate.

set -e

wait_for_proxy() {
    echo "Waiting for proxy..."
    sleep 2m & wait ${!}
}

wait_for_proxy

echo "Getting certificate..."

certbot certonly \
    --webroot \
    --webroot-path "/var/www/certbot" \
    -d "$DOMAIN" \
    --email "$ACME_DEFAULT_EMAIL" \
    --rsa-key-size 4096 \
    --agree-tos \
    --non-interactive \
    --staging \
    -v
