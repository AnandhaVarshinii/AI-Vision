"""
fetch_training_images.py — Bulk-source candidate training photos for the
three under-represented AI-Vision classes (Rice_Straw, Wheat_Husk,
Sugarcane_Bagasse) using the free Pexels API.

WHY THIS EXISTS
----------------
No public dataset of properly-labeled agricultural *residue/waste* photos
exists (confirmed via GitHub + Kaggle search). The original AI-Vision
dataset substituted "standing crop in a field" stock photos for these
3 classes, which is why the model confuses them. This script pulls real,
correctly-licensed photos and drops them straight into the dataset/raw/
folder structure that ai/prepare_dataset.py already knows how to ingest
(dedup, quality filter, resize, stratified split).

THIS MUST BE RUN ON YOUR OWN MACHINE, NOT INSIDE A SANDBOXED ENVIRONMENT
--------------------------------------------------------------------------
It needs outbound internet access to api.pexels.com.

SETUP
-----
1. Get a free API key (instant, no approval wait): https://www.pexels.com/api/
2. pip install requests
3. export PEXELS_API_KEY="your_key_here"     (or paste it into API_KEY below)
4. Run from your project root:
       python fetch_training_images.py --out dataset/raw --per-class 250

AFTER RUNNING
-------------
1. Skim through dataset/raw/<class>/ and delete any obviously wrong/irrelevant
   images (keyword search always pulls some noise — expect to remove ~10-20%).
   This script's per-query overlap also helps prepare_dataset.py's perceptual
   hash dedup discard near-duplicates automatically.
2. Run the existing pipeline to merge + clean + split into the real dataset:
       python ai/prepare_dataset.py --raw dataset/raw --out dataset
3. Retrain:
       python ai/train.py --data dataset --epochs 30 --batch 32
4. Re-check ai/evaluate.py or ai/cross_validate.py output — specifically the
   confusion matrix cells for Rice_Straw / Wheat_Husk / Sugarcane_Bagasse.
"""

import argparse
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("Install deps first:  pip install requests")
    sys.exit(1)

API_KEY = os.environ.get("PEXELS_API_KEY", "")  # or paste your key here directly
SEARCH_URL = "https://api.pexels.com/v1/search"

# Search terms per class, ordered from most-specific to most-generic.
# Specific terms first → higher quality matches; generic terms fill in volume.
QUERIES = {
    "rice_straw": [
        "rice straw pile",
        "rice stubble field after harvest",
        "stubble burning field",
        "paddy straw bales",
        "rice straw bundle",
        "harvested rice field stubble",
    ],
    "wheat_husk": [
        "wheat stubble field after harvest",
        "wheat straw bales",
        "wheat chaff pile",
        "wheat husk close up",
        "harvested wheat field stubble",
        "straw bale farm",
    ],
    "sugarcane_bagasse": [
        "sugarcane bagasse pile",
        "bagasse waste sugar mill",
        "crushed sugarcane residue",
        "sugarcane fiber waste",
        "sugar mill waste pile",
    ],
}

HEADERS = {}
TIMEOUT = 20
SLEEP_BETWEEN_CALLS = 1.0  # be polite to the free tier rate limit


def fetch_query(query, target_count, seen_ids):
    """Page through Pexels search results for one query, return list of (id, url)."""
    results = []
    page = 1
    per_page = 80  # Pexels max per_page
    while len(results) < target_count:
        params = {"query": query, "per_page": per_page, "page": page}
        try:
            resp = requests.get(SEARCH_URL, headers=HEADERS, params=params, timeout=TIMEOUT)
        except requests.RequestException as e:
            print(f"    ! request failed: {e}")
            break
        if resp.status_code == 429:
            print("    ! rate limited, sleeping 30s...")
            time.sleep(30)
            continue
        if resp.status_code != 200:
            print(f"    ! HTTP {resp.status_code}: {resp.text[:200]}")
            break
        data = resp.json()
        photos = data.get("photos", [])
        if not photos:
            break  # no more results for this query
        for p in photos:
            pid = p["id"]
            if pid in seen_ids:
                continue
            seen_ids.add(pid)
            # 'large' is a good balance of quality vs download size
            url = p["src"].get("large") or p["src"].get("original")
            results.append((pid, url))
        page += 1
        time.sleep(SLEEP_BETWEEN_CALLS)
        if page > 10:  # safety cap per query
            break
    return results


def download(url, dest_path):
    try:
        r = requests.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        dest_path.write_bytes(r.content)
        return True
    except requests.RequestException as e:
        print(f"    ! download failed ({url[:60]}...): {e}")
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="dataset/raw", help="Output root (matches prepare_dataset.py --raw)")
    parser.add_argument("--per-class", type=int, default=250, help="Target image count per class")
    args = parser.parse_args()

    if not API_KEY:
        print("ERROR: set PEXELS_API_KEY env var (or paste it into API_KEY in this script).")
        print("Get a free key instantly at https://www.pexels.com/api/")
        sys.exit(1)

    HEADERS["Authorization"] = API_KEY
    out_root = Path(args.out)

    for class_folder, queries in QUERIES.items():
        class_dir = out_root / class_folder
        class_dir.mkdir(parents=True, exist_ok=True)
        seen_ids = set()
        collected = []

        print(f"\n=== {class_folder} (target {args.per_class}) ===")
        per_query_target = max(20, args.per_class // len(queries))
        for q in queries:
            if len(collected) >= args.per_class:
                break
            print(f"  query: '{q}'")
            results = fetch_query(q, per_query_target, seen_ids)
            print(f"    found {len(results)} new candidates")
            collected.extend(results)

        collected = collected[: args.per_class]
        print(f"  downloading {len(collected)} images to {class_dir}/ ...")
        ok = 0
        for i, (pid, url) in enumerate(collected):
            if url is None:
                continue
            dest = class_dir / f"{class_folder}_{pid}.jpg"
            if dest.exists():
                ok += 1
                continue
            if download(url, dest):
                ok += 1
            time.sleep(0.3)
        print(f"  done: {ok}/{len(collected)} saved")

    print("\nAll classes processed.")
    print("Next steps:")
    print("  1. Manually skim dataset/raw/<class>/ folders and remove obvious mismatches")
    print("  2. python ai/prepare_dataset.py --raw dataset/raw --out dataset")
    print("  3. python ai/train.py --data dataset --epochs 30 --batch 32")


if __name__ == "__main__":
    main()
