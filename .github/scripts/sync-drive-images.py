"""
Downloads images from the Strange Times Google Drive folder into images/.
Each Drive file ID maps to a clean local filename.
To add new images: append to the IMAGES dict below.
"""

import os
import subprocess
import sys

IMAGES = {
    # Session area images
    "1MngNxIxy19izbLzt6CkMrUTIw8nqC5ba": "mass-grave.png",
    "1x6HWOWNmYBLZlydDrE_c0mkU6LkkvOHp": "strange-lab.png",
    "1szueg-Axuwslj5hE9ICcy1wwd053D-VG":  "ogzul-pack.png",
    "1ENCRaZuqVU96C7Fpr8sIJxX7cjHdRpAd": "ogzul-pack-alt.png",
    "1MS49xAhS2Ab-kWvK6pgSaBJaT0bXYg4B": "ogzul-and-pack.png",
    # Session cover
    "1WX2FmSlRJOqoU61Rk3-EVVrvEewX5Sow": "session1-cover.png",
    "10zw2ZZXUVQJBcZNqbC8pUdZcmojAGl-w": "session1-cover-tall.png",
    # Subject Seven
    "1UkdZLjY_dohASyD3IB8Rv70CAXtWISYt": "seven-human.png",
    "1QNzassn5wXVuYv8FtLlQbZjFLuCZv8V_": "seven-character-card.png",
    # Character card art (physical cards photographed)
    "1ea5v6F8NyqsUcteSJLR2hbDK_VEE8ind": "lucien-card.jpg",
    "17KXdMpn_mrDCQDb0_Qeg5zIfPPi0ziY_": "drogath-card.jpg",
    "1zS2bxaioFqGug5cl_DK2B7vbWV8XQw8L": "vaelis-card.jpg",
    # Misc
    "12ulLh3103CWfI4Zc1LfNzTW65Z5KhA_k": "mystery.png",
}

os.makedirs("images", exist_ok=True)

failed = []
skipped = []
downloaded = []

for file_id, dest in IMAGES.items():
    path = os.path.join("images", dest)
    if os.path.exists(path):
        skipped.append(dest)
        print(f"  skip  {dest}")
        continue

    print(f"  down  {dest} ...", flush=True)
    result = subprocess.run(
        ["gdown", "--fuzzy", "--no-cookies", file_id, "-O", path],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0 and os.path.exists(path) and os.path.getsize(path) > 1024:
        downloaded.append(dest)
        print(f"   ok   {dest} ({os.path.getsize(path) // 1024} KB)")
    else:
        if os.path.exists(path):
            os.remove(path)
        failed.append(dest)
        print(f"  FAIL  {dest}")
        if result.stderr:
            print("        " + result.stderr.strip()[:200])

print()
print(f"Downloaded: {len(downloaded)}  Skipped: {len(skipped)}  Failed: {len(failed)}")
if failed:
    print("Failed files:", ", ".join(failed))
    sys.exit(1)
