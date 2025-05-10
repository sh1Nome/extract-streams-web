#!/bin/sh

sh update_env.sh

docker-compose -f compose.yml -f compose.prod.yml up -d --build