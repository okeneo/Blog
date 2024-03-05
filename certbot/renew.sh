#!/bin/sh

set -e

cd /home/ec2-user/PersonalNest
/usr/local/bin/docker-compose -f docker-compose.prod.yml run --rm certbot certbot renew
