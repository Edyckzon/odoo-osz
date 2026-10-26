#!/bin/bash
# One-time installation, on the VPS. Does not modify Caddy or VPN services.
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo 'Run with sudo bash production/install-theme.sh'; exit 1; }
cd "$(dirname "$0")/.."
exec 9>/var/lock/osz-erp-deploy.lock
flock -n 9 || { echo 'Another OSZ deployment is running.'; exit 1; }
[[ -f production/.env ]] || { echo 'Production configuration not found.'; exit 1; }
[[ -z $(git status --porcelain --untracked-files=no) ]] || { echo 'Tracked files have local changes. Review before deploying.'; exit 1; }
dc() { docker compose --env-file production/.env -f production/compose.yaml "$@"; }
candidate="osz-erp:$(git rev-parse --short=12 HEAD)"
OSZ_IMAGE="$candidate" dc build odoo
dc exec -T db pg_isready -U postgres -d osz_erp

umask 077
backup="/opt/backups/osz-erp/$(date -u +%Y%m%dT%H%M%SZ)-muk"
mkdir -p "$backup"
chmod 700 "$backup"
cp production/.env "$backup/production.env"
cp -a production/secrets "$backup/secrets"
git rev-parse HEAD > "$backup/target-commit.txt"
stopped=0
trap 'if [[ $stopped == 1 ]]; then echo "Deployment interrupted. Odoo may be stopped. Backup: $backup. Do not delete volumes or rerun blindly; inspect the error before recovery." >&2; fi' EXIT
dc stop odoo
stopped=1
# Stop writers before taking the database + filestore pair.
dc exec -T db pg_dump -U postgres -Fc osz_erp > "$backup/database.dump"
dc run --rm -T --no-deps --entrypoint tar odoo -C /var/lib/odoo -czf - filestore > "$backup/filestore.tar.gz"
dc exec -T db pg_restore --list < "$backup/database.dump" > /dev/null
tar -tzf "$backup/filestore.tar.gz" > /dev/null
# Use the running release, which still contains the old launcher code, to uninstall it.
dc run --rm -T --no-deps odoo odoo shell -d osz_erp --no-http --workers=0 --max-cron-threads=0 <<'PYTHON'
m = env['ir.module.module'].search([('name', '=', 'osz_app_launcher'), ('state', '=', 'installed')])
if m:
    m.button_immediate_uninstall()
env.cr.commit()
PYTHON
OSZ_IMAGE="$candidate" dc run --rm -T --no-deps odoo odoo \
    -d osz_erp -i muk_web_theme -u osz_branding --without-demo=True --stop-after-init \
    --no-http --workers=0 --max-cron-threads=0

# Refresh branding dependencies BEFORE uninstalling the former theme.
OSZ_IMAGE="$candidate" dc run --rm -T --no-deps odoo odoo shell -d osz_erp --no-http --workers=0 --max-cron-threads=0 <<'PYTHON'
old = env['ir.module.module'].search([('name', '=', 'theme_liquid_glass'), ('state', '=', 'installed')])
if old:
    dependents = env['ir.module.module'].search([('state', '=', 'installed'), ('dependencies_id.name', '=', 'theme_liquid_glass')])
    assert not dependents, 'Liquid Glass still required by: ' + ', '.join(dependents.mapped('name'))
    old.button_immediate_uninstall()
for name in ('osz_branding', 'muk_web_theme'):
    assert env['ir.module.module'].search([('name', '=', name)]).state == 'installed', name
env.cr.commit()
PYTHON

# Persist the selected image only after successful module installation.
export OSZ_CANDIDATE_IMAGE="$candidate"
python3 - <<'PY'
import os
from pathlib import Path
p = Path('production/.env')
lines = [line for line in p.read_text().splitlines() if not line.startswith('OSZ_IMAGE=')]
lines.append('OSZ_IMAGE=' + os.environ['OSZ_CANDIDATE_IMAGE'])
tmp = p.with_name('.env.next')
tmp.write_text('\n'.join(lines) + '\n')
tmp.chmod(0o600)
tmp.replace(p)
PY
# The official image declares /mnt/extra-addons as an anonymous volume.
# Compose otherwise carries its OLD code into a recreated container.
# PostgreSQL and /var/lib/odoo use named volumes and are preserved by -V.
dc up -d --no-deps --force-recreate --renew-anon-volumes --wait --wait-timeout 120 odoo
dc exec -T odoo python3 - <<'PY'
from pathlib import Path
from urllib.request import urlopen
for path in (
    '/osz_branding/static/img/osz-erp.svg',
    '/muk_web_theme/static/src/webclient/navbar/navbar.js',
):
    assert Path('/mnt/extra-addons' + path).is_file(), path
    with urlopen('http://127.0.0.1:8069' + path, timeout=10) as response:
        assert response.status == 200, path
print('New theme and logo files are served successfully.')
PY
stopped=0
dc ps
echo "MuK and OSZ ERP identity installed. Local backup: $backup"
echo 'Refresh the browser and click the applications menu. This backup is not an off-site backup.'
