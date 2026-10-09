"""Strict player-package allowlist, integrity and private-content audit."""
import hashlib
import json
import os
import pathlib
import sys
import zipfile

APP = 'KirbyNightmareInDreamLandRecomp.exe'
BINARIES = {APP, 'SDL2.dll', 'libgcc_s_seh-1.dll', 'libstdc++-6.dll', 'libwinpthread-1.dll'}
ASSETS = {'assets/fonts/' + n for n in ('LatoLatin-Regular.ttf', 'LatoLatin-Bold.ttf', 'OpenMoji-black-glyf.ttf', 'NotoSansSymbols2-Regular.ttf')}
ASSETS |= {'assets/img/' + n for n in ('brand_mark.tga', 'verdict_ok.tga', 'verdict_warn.tga', 'verdict_bad.tga', 'verdict_none.tga', 'flags.png', 'pad_gba.tga')}
LICENSES = {'licenses/' + n + '.txt' for n in ('GBARecomp', 'RecompUI', 'ImGui', 'ArmRecompCore', 'RecompNet', 'Rbengine', 'SDL2', 'GCC-GPL3', 'GCC-LGPL3', 'GCC-Runtime-Exception', 'MinGW-Runtime', 'Font-Notices', 'Image-Notices', 'Lato-OFL', 'NotoSymbols-OFL', 'OpenMoji-LICENSE', 'JRickey-MIT', 'Reference-Integration', 'MPL-2.0', 'Framework-Attribution', 'TomlPlusPlus')}
LICENSES |= {'licenses/mpl-source/bios_hle.cpp', 'licenses/mpl-source/bios_hle.h'}
TOP = BINARIES | {'README.md', 'LICENSE.md', 'THIRD_PARTY_NOTICES.md', 'manifest.json'}
ALLOWED = TOP | ASSETS | LICENSES
PRIVATE_SHA1 = {'37a476567d133c146fee6b5e2eb0b07a215da6b0', '300c20df6731a33952ded8c436f7f186d25d3492'}

def audit(target):
    target = pathlib.Path(target)
    if target.suffix.lower() == '.zip':
        with zipfile.ZipFile(target) as z:
            entries = [(i.filename, z.read(i)) for i in z.infolist() if not i.is_dir()]
    else:
        entries = [(p.relative_to(target).as_posix(), p.read_bytes()) for p in sorted(target.rglob('*')) if p.is_file()]
    files = {}
    roots = [str(pathlib.Path(__file__).resolve().parents[2]), os.environ.get('USERPROFILE', ''), os.environ.get('MINGW_ROOT', '')]
    for name, data in entries:
        p = pathlib.PurePosixPath(name)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in name, f'Unsafe name: {name}'
        assert name not in files, f'Duplicate: {name}'
        assert name in ALLOWED, f'Not allowlisted: {name}'
        assert hashlib.sha1(data).hexdigest() not in PRIVATE_SHA1, f'Private input: {name}'
        for content in (data.lower(), data.decode('utf-16-le', errors='ignore').lower().encode()):
            content = content.replace(b'\\', b'/')
            assert not any(r and r.lower().replace('\\', '/').encode() in content for r in roots), f'Developer path: {name}'
        files[name] = data
    assert set(files) == ALLOWED, f'Missing files: {ALLOWED - set(files)}'
    manifest = json.loads(files['manifest.json'].decode('utf-8-sig'))
    assert {i['file'] for i in manifest} == ALLOWED - {'manifest.json'}
    assert len(manifest) == len(ALLOWED) - 1
    for item in manifest:
        data = files[item['file']]
        assert len(data) == item['bytes'] and hashlib.sha256(data).hexdigest() == item['sha256'], item['file']
    print(f'PASS: {len(files)} allowlisted files; manifest verified; no private assets or developer paths')
    return len(files)

if __name__ == '__main__':
    audit(sys.argv[1])
