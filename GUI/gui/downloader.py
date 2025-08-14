from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from urllib.request import urlopen, urlretrieve

GITHUB_RELEASE_API = "https://api.github.com/repos/mikf/gallery-dl/releases/latest"
GPG_KEY_URL = "https://github.com/mikf.gpg"


def ensure_gallery_dl(path: Path) -> None:
    """Ensure a gallery-dl binary exists at *path*.

    If the file is missing, download the latest release and verify its
    signature before moving it into place.
    """
    if path.exists():
        return

    release = json.load(urlopen(GITHUB_RELEASE_API))
    assets = {a["name"]: a["browser_download_url"] for a in release["assets"]}
    exe_url = assets.get("gallery-dl.exe")
    sig_url = assets.get("gallery-dl.exe.sig")
    if not exe_url or not sig_url:
        raise RuntimeError("gallery-dl.exe assets not found in release")

    with tempfile.TemporaryDirectory() as tmp:
        exe_tmp = Path(tmp) / "gallery-dl.exe"
        sig_tmp = Path(tmp) / "gallery-dl.exe.sig"
        urlretrieve(exe_url, exe_tmp)
        urlretrieve(sig_url, sig_tmp)

        key_data = urlopen(GPG_KEY_URL).read()
        subprocess.run(["gpg", "--batch", "--import"], input=key_data, check=True)
        subprocess.run(["gpg", "--verify", str(sig_tmp), str(exe_tmp)], check=True)

        sha256 = hashlib.sha256(exe_tmp.read_bytes()).hexdigest()
        print(f"Verified gallery-dl.exe with SHA256 {sha256}")

        path.parent.mkdir(parents=True, exist_ok=True)
        exe_tmp.replace(path)
