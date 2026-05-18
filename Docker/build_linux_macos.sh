#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

docker compose build

echo
echo "Image Docker creee : paginavox:gpu"
