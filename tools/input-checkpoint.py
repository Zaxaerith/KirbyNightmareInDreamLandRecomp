"""Small normal-input TCP checkpoint helper for the existing CSV replay.
No PC/memory writes or save states. Every request is recorded under logs/.
"""
import argparse
import json
import socket
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def png_rgb(path, width, height, pixels):
    if len(pixels) != width * height * 3:
        raise ValueError("Unexpected framebuffer format")
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data))
    rows = b"".join(b"\0" + pixels[y * width * 3:(y + 1) * width * 3] for y in range(height))
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b""))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=19847)
    parser.add_argument("--name", required=True)
    parser.add_argument("--csv", type=Path)
    parser.add_argument("--until", type=int)
    parser.add_argument("--capture", default="")
    parser.add_argument("--keys", type=lambda x: int(x, 0))
    parser.add_argument("--frames", type=int, default=0)
    parser.add_argument("--checkpoints", default="")
    parser.add_argument("--quit", action="store_true")
    args = parser.parse_args()
    if not args.name.replace("-", "").replace("_", "").isalnum():
        parser.error("Use a simple session name")
    if args.frames < 0 or args.frames > 1200 or (args.until is not None and not 0 <= args.until <= 15000):
        parser.error("Bound this operation to <=1200 new frames, or <=15000 absolute CSV frames")
    folder = ROOT / "logs" / args.name
    folder.mkdir(parents=True, exist_ok=True)
    with socket.create_connection(("127.0.0.1", args.port), timeout=10) as sock, sock.makefile("rb") as stream, (folder / "commands.jsonl").open("a", encoding="utf-8") as log:
        sock.settimeout(55)
        def request(command):
            sock.sendall((json.dumps(command) + "\n").encode())
            response = json.loads(stream.readline())
            recorded = {k: v for k, v in response.items() if k != "data"}
            if "data" in response:
                recorded["data_bytes"] = len(response["data"]) // 2
            log.write(json.dumps({"request": command, "response": recorded}) + "\n")
            log.flush()
            if not response.get("ok"):
                raise RuntimeError(response)
            return response
        def frame():
            return request({"cmd": "frame"})["frame"]
        def advance(target, keys):
            current = frame()
            request({"cmd": "set_keyinput", "value": keys})
            while current < target:
                reply = request({"cmd": "run_frames", "n": min(target - current, 120), "keyinput": keys})
                after = reply["frame"]
                if after < current or (after == current and reply["frames"] == 0):
                    raise RuntimeError("No forward progress")
                current = after
            return current
        def capture(label):
            if not label.replace("-", "").replace("_", "").isalnum():
                raise ValueError("Use a simple capture label")
            observed = frame()
            response = request({"cmd": "screenshot"})
            path = folder / f"{label}-f{observed}.png"
            png_rgb(path, response["w"], response["h"], bytes.fromhex(response["data"]))
            metadata = {"frame": observed, "image": str(path), "ppu": request({"cmd": "ppu_state"})}
            (folder / f"{label}-f{observed}.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
            print(json.dumps({"capture": str(path), "frame": observed}), flush=True)
        if args.csv:
            if args.until is None:
                parser.error("CSV requires --until")
            events = []
            for line in args.csv.read_text(encoding="utf-8-sig").splitlines():
                if line and not line.startswith("#"):
                    number, keys = line.split(",")
                    events.append((int(number), int(keys, 0)))
            if not events or events != sorted(events):
                raise ValueError("CSV events must be ordered")
            checkpoints = sorted(int(value) for value in args.checkpoints.split(",") if value)
            current = frame()
            boundaries = sorted({args.until} | {event[0] for event in events if current < event[0] < args.until} | {value for value in checkpoints if current < value <= args.until})
            for target in boundaries:
                keys = next((keys for number, keys in reversed(events) if number <= current), 0x3FF)
                current = advance(target, keys)
                if current in checkpoints:
                    capture("checkpoint")
        elif args.frames:
            if args.keys is None or not 0 <= args.keys <= 0x3FF:
                parser.error("Frames requires a valid active-low --keys")
            advance(frame() + args.frames, args.keys)
        if args.capture:
            capture(args.capture)
        if args.quit:
            print(json.dumps(request({"cmd": "quit"})), flush=True)
        else:
            print(json.dumps({"frame": frame()}), flush=True)

if __name__ == "__main__":
    main()
