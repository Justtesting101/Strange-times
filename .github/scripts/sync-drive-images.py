"""
Downloads every image in the Strange Times Google Drive images folder.
Just add an image to the Drive folder and re-run the workflow — no code changes needed.
Filenames are sanitized to lowercase-with-hyphens for web use.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

FOLDER_ID = "1vLxDomJrI2TNngYHlIfr-6jDLxalH6bZ"


def sanitize(filename):
    stem, _, ext = filename.rpartition(".")
    stem = stem.lower()
    stem = re.sub(r"['\"]", "", stem)           # drop apostrophes/quotes
    stem = re.sub(r"[^a-z0-9]+", "-", stem)    # non-alphanumeric → hyphen
    stem = stem.strip("-")
    return f"{stem}.{ext.lower()}" if ext else stem


os.makedirs("images", exist_ok=True)

with tempfile.TemporaryDirectory() as tmp:
    print(f"Fetching folder {FOLDER_ID} ...")
    result = subprocess.run(
        ["gdown", "--folder", FOLDER_ID, "-O", tmp],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("gdown failed:")
        print(result.stderr[-500:])
        sys.exit(1)

    # gdown puts files inside a subfolder named after the Drive folder
    all_files = []
    for root, _, files in os.walk(tmp):
        for f in files:
            all_files.append(os.path.join(root, f))

    if not all_files:
        print("No files were downloaded.")
        sys.exit(0)

    downloaded, skipped = [], []

    for src in sorted(all_files):
        clean = sanitize(os.path.basename(src))
        dest = os.path.join("images", clean)

        # Skip tiny files — likely an error/redirect page, not a real image
        if os.path.getsize(src) < 2048:
            print(f"  skip  {clean}  (file too small, probably an error)")
            continue

        if os.path.exists(dest):
            skipped.append(clean)
            print(f"  skip  {clean}")
        else:
            shutil.copy2(src, dest)
            downloaded.append(clean)
            print(f"   new  {clean}  ({os.path.getsize(dest) // 1024} KB)")

print()
print(f"New: {len(downloaded)}  Already present: {len(skipped)}")
if downloaded:
    print("Added:", ", ".join(downloaded))
