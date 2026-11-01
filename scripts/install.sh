#!/usr/bin/env bash
# Cai ERPNext v15 + app omigos_erp.
# Yeu cau: bench (https://frappeframework.com/docs/user/en/installation), Python 3.10-3.12, Node 18+, MariaDB, Redis.
# Bien moi truong tuy chon: SITE (mac dinh omigos.localhost), DB_ROOT_PASSWORD, ADMIN_PASSWORD.
set -euo pipefail

SITE="${SITE:-omigos.localhost}"
DB_ROOT_PASSWORD="${DB_ROOT_PASSWORD:?Hay dat DB_ROOT_PASSWORD (mat khau root cua MariaDB)}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-admin}"
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# bench get-app can mot git repo co pyproject.toml o goc, nen dong goi thu muc app thanh repo tam.
APP_SRC="$(mktemp -d)"
cp -r "$REPO_DIR/omigos_erp/." "$APP_SRC/"
git -C "$APP_SRC" init -q
git -C "$APP_SRC" add -A
git -C "$APP_SRC" -c commit.gpgsign=false -c user.email=build@local -c user.name=build commit -qm "omigos_erp"

bench init --frappe-branch version-15 frappe-bench
cd frappe-bench
bench get-app --branch version-15 https://github.com/frappe/erpnext
bench new-site "$SITE" --db-root-password "$DB_ROOT_PASSWORD" --admin-password "$ADMIN_PASSWORD"
bench --site "$SITE" install-app erpnext
bench get-app "$APP_SRC"
bench --site "$SITE" install-app omigos_erp
bench --site "$SITE" migrate

echo
echo "Xong. Chay: cd frappe-bench && bench start   (can bat worker nen de tinh lai gia tri ton kho)"
echo "Mo http://$SITE:8000  (Administrator / $ADMIN_PASSWORD), chon ngon ngu Vietnamese o Setup Wizard."
