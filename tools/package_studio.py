"""Build a reproducible source ZIP and verify its contents against the checkout."""
import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
studio = ROOT / 'Amber_Studio'
files = sorted(p for p in studio.rglob('*') if p.is_file() and p.name != 'SHA256SUMS.txt'
               and not any(part in {'__pycache__', 'studio_data', 'build', 'dist'} for part in p.relative_to(studio).parts))
manifest = ''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(studio).as_posix()}\n' for p in files)
(studio / 'SHA256SUMS.txt').write_text(manifest)
files.append(studio / 'SHA256SUMS.txt')
for folder in ['tests', 'tools', 'docs']:
    files.extend(p for p in (ROOT / folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
files.extend(ROOT / name for name in ['README.md', 'requirements-dev.txt', '.gitignore'])
release = ROOT / 'releases/Amber_Studio_Afterhours_Source.zip'
release.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(release, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for p in sorted(files):
        info = zipfile.ZipInfo(p.relative_to(ROOT).as_posix(), date_time=(2026, 10, 30, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        z.writestr(info, p.read_bytes())
with zipfile.ZipFile(release) as z:
    assert z.testzip() is None
    for name in z.namelist():
        assert z.read(name) == (ROOT / name).read_bytes(), name
digest = hashlib.sha256(release.read_bytes()).hexdigest()
(release.parent / 'SHA256SUMS.txt').write_text(f'{digest}  {release.name}\n')
print(f'Verified {len(files)} archived files; {release.stat().st_size} bytes; SHA-256 {digest}')
