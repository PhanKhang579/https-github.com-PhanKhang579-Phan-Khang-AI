#!/usr/bin/env bash
# Cai ERPNext + app omigos_erp. Yeu cau: bench da cai (https://frappeframework.com/docs/user/en/installation)
set -euo pipefail
bench init --frappe-branch version-15 frappe-bench
cd frappe-bench
bench get-app --branch version-15 erpnext
bench new-site omigos.localhost --admin-password admin
bench --site omigos.localhost install-app erpnext
bench get-app omigos_erp "$(dirname "$0")/../omigos_erp"
bench --site omigos.localhost install-app omigos_erp
bench start
