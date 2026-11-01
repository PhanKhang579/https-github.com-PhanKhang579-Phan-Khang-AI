# Anh ERPNext v15 + app omigos_erp. Build tu thu muc goc repo:
#   docker build -f docker/Dockerfile -t omigos-erp:v15 .
FROM frappe/erpnext:v15.124.3

COPY --chown=frappe:frappe omigos_erp /home/frappe/frappe-bench/apps/omigos_erp
RUN /home/frappe/frappe-bench/env/bin/python -m pip install --no-cache-dir -e /home/frappe/frappe-bench/apps/omigos_erp
