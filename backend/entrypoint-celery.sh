#!/bin/sh

celery -A myproject worker -l INFO
