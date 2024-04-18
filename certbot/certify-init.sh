#!/bin/sh

# Waits for nginx to be available, then gets the first certificate.

set -e

until nc -z nginx 80; do
    echo "Waiting for nginx..."
    sleep 5s
done

echo "Getting certificate..."

certbot certonly \
    --webroot \
    --webroot-path "/var/www/certbot" \
    -d "$DOMAIN" \
    -d "www.$DOMAIN" \
    --email "$ACME_DEFAULT_EMAIL" \
    --rsa-key-size 4096 \
    --agree-tos \
    --non-interactive \
    -v
