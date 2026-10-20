"""Generate local secrets once; never overwrite an existing installation."""
from pathlib import Path
import secrets

root = Path(__file__).resolve().parents[1]
targets = [root / '.env', root / 'config/odoo.conf', root / 'postgres-init/01-odoo-role.sql']
if any(path.exists() for path in targets):
    raise SystemExit('Existing configuration found. No files changed.')
postgres, odoo, master = (secrets.token_hex(32) for _ in range(3))
contents = [
    f'POSTGRES_PASSWORD={postgres}\nODOO_DB_PASSWORD={odoo}\n',
    '[options]\naddons_path = /mnt/extra-addons\ndata_dir = /var/lib/odoo\n'
    f'admin_passwd = {master}\nworkers = 0\nmax_cron_threads = 1\n'
    'proxy_mode = False\nhttp_interface = 0.0.0.0\n',
    f"CREATE ROLE odoo WITH LOGIN PASSWORD '{odoo}' CREATEDB NOSUPERUSER NOCREATEROLE;\n",
]
for path, content in zip(targets, contents):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        stream.write(content)
    path.chmod(0o600)
print('Local configuration created. Credentials are in ignored files; do not commit them.')
