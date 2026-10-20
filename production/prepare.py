"""Linux only. Run with sudo; generate configuration, never start services."""
import os
from pathlib import Path
import secrets
import subprocess

if os.name != 'posix' or os.geteuid() != 0:
    raise SystemExit('Run with sudo python3 production/prepare.py on Linux.')
root = Path(__file__).resolve().parent
if (root / '.env').exists() or (root / 'secrets').exists():
    raise SystemExit('Existing configuration found. No files changed.')
revision = subprocess.check_output(['git', '-C', str(root.parent), 'rev-parse', '--short=12', 'HEAD'], text=True).strip()
postgres, password, master = (secrets.token_hex(32) for _ in range(3))
os.umask(0o077)
(root / '.env').write_text(f'POSTGRES_PASSWORD={postgres}\nODOO_DB_PASSWORD={password}\nOSZ_IMAGE=osz-erp:{revision}\n')
(root / 'secrets').mkdir(mode=0o700)
config = root / 'secrets/odoo.conf'
config.write_text(f'''[options]
admin_passwd = {master}
addons_path = /mnt/extra-addons
data_dir = /var/lib/odoo
db_host = db
db_user = odoo
db_password = {password}
db_name = osz_erp
dbfilter = ^osz_erp$
list_db = False
proxy_mode = True
workers = 2
max_cron_threads = 1
limit_memory_soft = 536870912
limit_memory_hard = 805306368
limit_time_cpu = 60
limit_time_real = 120
''')
# UID/GID verified in the pinned official Odoo image; host parent stays root-only.
os.chown(config, 100, 101)
print('Configuration prepared. No services or networks changed. Keep secrets out of Git.')
