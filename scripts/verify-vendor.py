"""Verify pinned upstream modules, ignoring runtime Python caches."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for lock_path in sorted((root / 'third-party').glob('*.lock.json')):
    lock = json.loads(lock_path.read_text())
    names = lock.get('modules') or [lock['module']]
    extensions = set(lock.get('text_extensions', ['.py', '.js', '.xml', '.scss', '.rst', '.md', '.txt', '.svg', '.html']))
    actual = {}
    for name in names:
        for path in (root / 'custom-addons' / name).rglob('*'):
            if not path.is_file() or '__pycache__' in path.parts or path.suffix == '.pyc':
                continue
            data = path.read_bytes()
            if path.suffix in extensions:
                data = data.replace(b'\r\n', b'\n')
            actual[path.relative_to(root).as_posix()] = hashlib.sha256(data).hexdigest()
    if actual != lock['sha256']:
        raise SystemExit(f'{lock_path.name}: upstream differs from its lock. Review changes.')
    print(f"Verified {lock_path.name}: {lock['commit']}")
