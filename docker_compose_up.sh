#!/bin/sh

docker-compose -f compose.yml -f compose.prod.yml up -d --build