#!/usr/bin/env bash
# Sao luu CSDL + file dinh kem. Chay trong thu muc docker/. Ket qua nam trong volume "sites" (sites/<SITE>/private/backups).
set -euo pipefail
cd "$(dirname "$0")"
SITE="$(grep -E '^SITE_NAME=' .env | cut -d= -f2)"
docker compose exec backend bench --site "${SITE:-erp.localhost}" backup --with-files
docker compose exec backend ls -lh "sites/${SITE:-erp.localhost}/private/backups" | tail -5
