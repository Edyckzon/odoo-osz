#!/bin/bash
# One-time installation, on the VPS. Does not modify Caddy or VPN services.
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo 'Run with sudo bash production/install-launcher.sh'; exit 1; }
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
backup="/opt/backups/osz-erp/$(date -u +%Y%m%dT%H%M%SZ)-launcher"
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
OSZ_IMAGE="$candidate" dc run --rm -T --no-deps odoo odoo \
    -d osz_erp -i osz_app_launcher --without-demo=True --stop-after-init \
    --no-http --workers=0 --max-cron-threads=0

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
dc up -d --no-deps --wait --wait-timeout 120 odoo
stopped=0
dc ps
echo "Launcher installed. Local backup: $backup"
echo 'Refresh the browser and click the applications icon. This backup is not an off-site backup.'
