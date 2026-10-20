#!/bin/bash
set -euo pipefail
psql -v ON_ERROR_STOP=1 --username postgres --dbname postgres <<'SQL'
\getenv odoo_password ODOO_DB_PASSWORD
CREATE ROLE odoo LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE PASSWORD :'odoo_password';
CREATE DATABASE osz_erp OWNER odoo;
SQL
