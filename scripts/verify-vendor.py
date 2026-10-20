"""Verify the untouched, pinned upstream theme, ignoring runtime Python caches."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
lock = json.loads((root / 'third-party/liquid-glass.lock.json').read_text())
module = root / 'custom-addons' / lock['module']
actual = {
    path.relative_to(root).as_posix(): hashlib.sha256(
        path.read_bytes().replace(b'\r\n', b'\n')
        if path.suffix in {'.py', '.js', '.xml', '.scss', '.rst', '.md', '.txt', '.svg', '.html'}
        else path.read_bytes()
    ).hexdigest()
    for path in module.rglob('*')
    if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc'
}
if actual != lock['sha256']:
    raise SystemExit('Upstream theme differs from its lock. Review and record changes explicitly.')
print('Verified Liquid Glass upstream commit ' + lock['commit'])
