#!/usr/bin/env python3
"""Standard-library bootstrap for a cached isolated runtime, never global pip."""

import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import venv


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-dir", type=Path, help="Optional isolated environment location")
    parser.add_argument("--offline", action="store_true", help="Require an already provisioned runtime; never install")
    parser.add_argument("--setup-only", action="store_true")
    parser.add_argument("renderer_args", nargs=argparse.REMAINDER, help="After --, arguments for render_study_guide.py")
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        parser.error("Python 3.11+ is required")
    scripts = Path(__file__).resolve().parent
    lock = scripts / "requirements.lock"
    fingerprint = hashlib.sha256(lock.read_bytes() + f"{sys.version_info[:2]}".encode()).hexdigest()[:16]
    cache = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / ".cache"))) if os.name == "nt" else Path(os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache")))
    runtime = (args.runtime_dir or cache / "OHamdy-agent-skills" / "renderer" / fingerprint).expanduser().resolve()
    if runtime.is_relative_to(scripts.parent.parents[1]):
        parser.error("Runtime directory must be outside the installed skill")
    python = runtime / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    marker = runtime / "renderer-lock.txt"
    owner = runtime / "renderer-owner.txt"
    ownership = "OHamdy cufe-study-guide renderer\n"
    try:
        ready = python.exists() and marker.exists() and marker.read_text(encoding="utf-8").strip() == fingerprint
        if not ready:
            if args.offline:
                raise RuntimeError("No matching cached renderer runtime; provision it once with network access, or use a capable native renderer")
            if runtime.exists() and any(runtime.iterdir()) and (not owner.exists() or owner.read_text(encoding="utf-8") != ownership):
                raise RuntimeError("Runtime directory is occupied by an unrelated environment; choose a new --runtime-dir")
            runtime.mkdir(parents=True, exist_ok=True)
            owner.write_text(ownership, encoding="utf-8")
            print("Preparing isolated study-guide renderer dependencies...", flush=True)
            venv.EnvBuilder(with_pip=True).create(runtime)
            completed = subprocess.run([str(python), "-m", "pip", "install", "--disable-pip-version-check", "--quiet", "--require-hashes", "-r", str(lock)], check=False)
            if completed.returncode:
                raise RuntimeError("Dependency installation failed; inspect pip diagnostics and retry the same bootstrap")
            marker.write_text(fingerprint + "\n", encoding="utf-8")
        if args.setup_only:
            print(f"Renderer runtime ready: {python}")
            return 0
        forwarded = args.renderer_args
        if forwarded[:1] == ["--"]:
            forwarded = forwarded[1:]
        if not forwarded:
            parser.error("Pass renderer arguments after --, or use --setup-only")
        return subprocess.run([str(python), str(scripts / "render_study_guide.py"), *forwarded], check=False).returncode
    except (OSError, RuntimeError) as exc:
        print(f"Renderer runtime unavailable: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
