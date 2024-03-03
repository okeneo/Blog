#!/bin/sh

# Waits for the proxy to be available, then gets the first certificate.

set -e

until nc -z nginx 80; do
    echo "Waiting for proxy..."
    sleep 5s & wait ${!}
done

echo "Getting certificate..."

certbot certonly \
    --webroot \
    --webroor-path "/var/www/certbot" \
    -d "$DOMAIN" \
    --email $EMAIL \
    --rsa-key-size 4096 \
    --agree-tos \
    -noninteractive
