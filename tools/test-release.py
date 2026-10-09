"""Bounded ZIP acceptance: isolated installation, PATH, assets and save copies."""
import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil
import struct
import subprocess
import time
import zipfile
import zlib

root = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('zip', type=pathlib.Path)
parser.add_argument('--rom', type=pathlib.Path, required=True)
parser.add_argument('--bios', type=pathlib.Path, required=True)
parser.add_argument('--save', type=pathlib.Path, required=True, help='Copy of game-visible verified native SRAM')
args = parser.parse_args()
archive = args.zip.resolve()
subprocess.run([os.sys.executable, str(root / 'tools/audit-release.py'), str(archive)], check=True)
scratch = root / 'release-test' / f'{archive.stem}-{time.time_ns()}'
installed = scratch / 'installed'
outside = scratch / 'unrelated-working-directory'
private = scratch / 'private-inputs'
for p in (installed, outside, private):
    p.mkdir(parents=True)
with zipfile.ZipFile(archive) as zipped:
    zipped.extractall(installed)
exe = installed / 'KirbyNightmareInDreamLandRecomp.exe'
assert not (installed / 'game.toml').exists()
rom, bios = private / 'own-rom.gba', private / 'own-bios.bin'
shutil.copyfile(args.rom, rom)
shutil.copyfile(args.bios, bios)
assert hashlib.sha1(rom.read_bytes()).hexdigest() == '37a476567d133c146fee6b5e2eb0b07a215da6b0'
assert hashlib.sha1(bios.read_bytes()).hexdigest() == '300c20df6731a33952ded8c436f7f186d25d3492'
original_save_hash = hashlib.sha256(args.save.read_bytes()).hexdigest()
test_save = scratch / 'native-progress.sav'
shutil.copyfile(args.save, test_save)
assert test_save.stat().st_size == 32768
env = os.environ.copy()
for name in list(env):
    if name.startswith(('GBARECOMP_', 'LNG_')):
        del env[name]
env['PATH'] = os.environ['SystemRoot'] + '\\System32'
results = {}

def run(name, options, replay=None, expect=0, custom_env=None, timeout=60):
    local_env = env.copy()
    local_env['GBARECOMP_COVERAGE_JSON'] = str(scratch / f'{name}-coverage.json')
    local_env['GBARECOMP_MISS_FRAG'] = str(scratch / f'{name}-misses.toml.frag')
    if replay:
        local_env['GBARECOMP_INPUT_REPLAY'] = str(replay)
    if custom_env:
        local_env.update(custom_env)
    process = subprocess.Popen([str(exe), *options], cwd=outside, env=local_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        raise AssertionError(f'{name}: bounded timeout; process stopped')
    output = (stdout + stderr).decode('utf-8', errors='replace')
    (scratch / f'{name}.log').write_text(output, encoding='utf-8')
    assert process.returncode == expect, f'{name}: exit {process.returncode}; {output[-1500:]}'
    results[name] = {'exit': process.returncode, 'pid': process.pid}
    return output

def launcher(name, views=False):
    script = f'wait:5;shot:{scratch / (name + ".png")};'
    if views:
        script += f'view:settings;wait:3;shot:{scratch / "settings.png"};view:controller;wait:3;shot:{scratch / "controller.png"};'
    script += 'quit'
    output = run(name, [], custom_env={'LNG_SCRIPT': script, 'LNG_TEST_HIDDEN': '1', 'LNG_SMOKE_FRAMES': '80'}, timeout=25)
    assert '[dbg] script:' in output and 'rom_loaded' not in output
    assert 'SDL_CreateWindow failed' not in output and 'SDL_GL_CreateContext failed' not in output
    assert (scratch / f'{name}.png').is_file()
    results[name].update(hidden_renderer=True, game_not_booted=True)

# Actual first-run renderer from clean ZIP; cached paths are added only afterwards.
launcher('first-launch-no-assets')
(installed / 'rom.cfg').write_text(str(rom) + '\n')
(installed / 'bios.cfg').write_text(str(bios) + '\n')
launcher('cached-launcher', views=True)

wrong_rom, wrong_bios = private / 'wrong.gba', private / 'wrong-bios.bin'
wrong_rom.write_bytes(bytes(8388608))
wrong_bios.write_bytes(bytes(16384))
# Model uses the exact linked launcher implementation, not duplicate hash logic.
contract = subprocess.run([str(root / 'build/host/launcher_contract.exe'), str(rom), str(bios), str(wrong_rom), str(wrong_bios), str(scratch / 'contract')],
                          cwd=outside, env=env, capture_output=True, timeout=25)
contract_text = (contract.stdout + contract.stderr).decode('utf-8', errors='replace')
(scratch / 'launcher-contract.log').write_text(contract_text, encoding='utf-8')
assert contract.returncode == 0 and 'PASS:' in contract_text, contract_text
results['launcher-contract'] = {'exit': 0, 'valid_wrong_missing_inputs': 'PASS', 'settings_path_cache_persistence': 'PASS'}
output = run('wrong-rom', ['--rom', str(wrong_rom), '--bios', str(bios), '--no-window', '--frames', '1', '--save', str(test_save)], expect=1)
assert 'mismatch' in output.lower() or 'sha1' in output.lower()
assert (installed / 'rom.cfg').read_text().strip() == str(rom), 'Rejected ROM must not replace valid cache'
output = run('wrong-bios', ['--rom', str(rom), '--bios', str(wrong_bios), '--no-window', '--frames', '1', '--save', str(test_save)], expect=1)
assert 'mismatch' in output.lower() or 'sha1' in output.lower()
assert (installed / 'bios.cfg').read_text().strip() == str(bios), 'Rejected BIOS must not replace valid cache'

def rgb_hash(path):
    # Standard-library PNG decoding, for deterministic game-visible comparison.
    png = path.read_bytes()
    assert png[:8] == b'\x89PNG\r\n\x1a\n'
    offset, compressed = 8, b''
    while offset < len(png):
        length = struct.unpack('>I', png[offset:offset+4])[0]
        kind, data = png[offset+4:offset+8], png[offset+8:offset+8+length]
        if kind == b'IHDR':
            width, height, depth, color, _, _, interlace = struct.unpack('>IIBBBBB', data)
        if kind == b'IDAT':
            compressed += data
        offset += length + 12
    assert depth == 8 and color in (2, 6) and interlace == 0
    channels = 3 if color == 2 else 4
    raw, previous, rgb = zlib.decompress(compressed), bytearray(width * channels), bytearray()
    for y in range(height):
        start = y * (width * channels + 1)
        mode, row = raw[start], bytearray(raw[start+1:start+1+width*channels])
        for x in range(len(row)):
            a, b, c = row[x-channels] if x >= channels else 0, previous[x], previous[x-channels] if x >= channels else 0
            p = a + b - c
            pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)
            predictor = (0, a, b, (a+b)//2, a if pa <= pb and pa <= pc else b if pb <= pc else c)[mode]
            row[x] = (row[x] + predictor) & 255
        for x in range(0, len(row), channels):
            rgb.extend(row[x:x+3])
        previous = row
    return hashlib.sha256(rgb).hexdigest()

def smoke(name, frames, save, replay, baseline):
    image = scratch / f'{name}.png'
    output = run(name, ['--no-window', '--frames', str(frames), '--save', str(save), '--dump-png', str(image)], replay)
    assert f'ppu_frames={frames}' in output and 'failed=0' in output
    assert 'unmapped=0' in output and 'io_unhandled=0' in output
    pixel_hash = rgb_hash(image)
    results[name].update(frames=frames, rgb_sha256=pixel_hash, save_bytes=save.stat().st_size,
                         coverage=re.search(r'self_heal_coverage=[^\r\n]+', output)[0])
    if baseline.is_file():
        assert pixel_hash == rgb_hash(baseline), f'{name}: baseline pixel mismatch; inspect {image}'
        results[name]['prior_gameplay_pixels'] = 'IDENTICAL'

smoke('title', 720, scratch / 'fresh-title.sav', None, root / 'logs/title720.png')
smoke('first-stage-entry', 2800, scratch / 'fresh-entry.sav', root / 'tools/first-actions.csv', root / 'logs/level2800.png')
# Load real saved progress, normal exit/flush, then a second new process reads it.
smoke('native-map', 2660, test_save, root / 'tools/native-load.csv', root / 'logs/round2-reload/unlocked-stage-two-f2660.png')
save_after_flush = hashlib.sha256(test_save.read_bytes()).hexdigest()
smoke('native-cold-menu', 1200, test_save, root / 'tools/native-load.csv', root / 'logs/round2-reload/checkpoint-f1200.png')
assert hashlib.sha256(test_save.read_bytes()).hexdigest() == save_after_flush == original_save_hash
assert hashlib.sha256(args.save.read_bytes()).hexdigest() == original_save_hash
assert not (outside / 'saves').exists()
assert (installed / 'rom.cfg').read_text().strip() == str(rom)
assert (installed / 'bios.cfg').read_text().strip() == str(bios)
report = {'version': 'v0.1.0-preview', 'zip': archive.name, 'zip_bytes': archive.stat().st_size,
          'zip_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(), 'pristine_package_files': len(json.loads((installed / 'manifest.json').read_text(encoding='utf-8-sig'))) + 1,
          'isolated_zip_installation': True, 'developer_tools_removed_from_path': True, 'external_working_directory': True,
          'game_toml_required': False, 'original_save_unchanged': True, 'native_sram_sha256': save_after_flush,
          'results': results, 'full_clear_replay_repeated': False,
          'manual_launcher_and_keyboard': 'PENDING', 'owner_controller_graphics_basic_audio': 'Previously confirmed by owner',
          'native_save_scope': 'Existing 1%/stage-2 progress retained across normal exit and fresh processes; no new stage clear in this round'}
(root / 'docs/RELEASE_TEST_RESULT.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
(scratch / 'result.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, indent=2))
