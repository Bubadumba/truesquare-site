#!/usr/bin/env python3
"""Generate an illustration with the OpenAI Images API and register it in content/photos.json.

Two steps, so a person (or the agent) can look at the candidates before one is kept:

  A) candidates
     python3 tools/generate_image.py --prompt-file content/research/<slug>-image-hero.txt \
         --slot hero --size 1536x1024 --n 3 --tmp /tmp/img-<id>
     -> writes /tmp/img-<id>/candidate-1.png ... and prints the paths plus the API "usage" object (tokens).

  B) pick
     python3 tools/generate_image.py --pick 2 --tmp /tmp/img-<id> --id ai-<slug>-hero \
         --out public/img/blog/ai/<slug>-hero.webp --shows "..." --alt "..." --room bath --slot hero \
         --prompt-file content/research/<slug>-image-hero.txt
     -> converts the chosen candidate to WebP (max 1600 px, quality 82, no EXIF), writes the IPTC
        DigitalSourceType tag with ExifTool when it is installed, and appends an entry to content/photos.json.

Authentication: the header "Authorization: Bearer $OPENAI_API_KEY" is sent ONLY when that variable is set.
In a Claude Code cloud environment the key is a network secret for api.openai.com (the proxy adds it, the
variable is empty). In GitHub Actions it is the OPENAI_API_KEY secret. The key is never printed.

The allowed values for --size and --quality come from the OpenAI image generation guide
(https://developers.openai.com/api/docs/guides/image-generation); this script passes them through unchanged.
The model comes from content/config.yaml (images.model). Prices are per token; the "usage" object is printed
so each run can report its cost.
"""
import argparse
import base64
import datetime
import json
import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blogcore as bc  # noqa: E402

API_URL = "https://api.openai.com/v1/images/generations"
AI_DIR = os.path.join(bc.PUB, "img", "blog", "ai")
IPTC_URI = "http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia"


def die(msg, code=1):
    print("ERROR:", msg, file=sys.stderr)
    sys.exit(code)


def generate(args):
    import requests
    cfg = bc.load_config()
    model = (cfg.get("images") or {}).get("model") or "gpt-image-2.5-flare"
    with open(args.prompt_file, encoding="utf-8") as f:
        prompt = f.read().strip()
    if not prompt:
        die("the prompt file is empty")
    os.makedirs(args.tmp, exist_ok=True)
    payload = {"model": model, "prompt": prompt, "n": args.n, "size": args.size, "quality": args.quality,
               "output_format": "png"}
    headers = {"Content-Type": "application/json"}
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key:
        headers["Authorization"] = "Bearer " + key
    last = None
    for attempt in range(3):
        try:
            r = requests.post(API_URL, headers=headers, json=payload, timeout=180)
        except requests.RequestException as e:
            last = f"network error: {e}"
            time.sleep(5)
            continue
        if r.status_code == 200:
            break
        last = f"HTTP {r.status_code}: {r.text[:400]}"
        if r.status_code in (400, 401, 403):
            break
        time.sleep(5)
    else:
        die(last or "no response")
    if r.status_code != 200:
        die(last)
    data = r.json()
    paths = []
    for i, item in enumerate(data.get("data", []), start=1):
        b64 = item.get("b64_json")
        if not b64:
            continue
        p = os.path.join(args.tmp, f"candidate-{i}.png")
        with open(p, "wb") as f:
            f.write(base64.b64decode(b64))
        paths.append(p)
    if not paths:
        die("the API returned no images")
    print("candidates:")
    for p in paths:
        print(" ", p)
    print("usage:", json.dumps(data.get("usage", {})))
    print("model:", model)


def pick(args):
    from PIL import Image
    out = os.path.abspath(args.out)
    if not out.startswith(os.path.abspath(AI_DIR) + os.sep) or not out.endswith(".webp"):
        die(f"--out must be a .webp file under public/img/blog/ai/ (got {args.out})")
    for name in ("id", "shows", "alt", "room", "slot", "prompt_file"):
        if not getattr(args, name):
            die(f"--{name.replace('_', '-')} is required for --pick")
    src = os.path.join(args.tmp, f"candidate-{args.pick}.png")
    if not os.path.isfile(src):
        die(f"{src} does not exist")
    with open(args.prompt_file, encoding="utf-8") as f:
        prompt = f.read().strip()
    cfg = bc.load_config()
    model = (cfg.get("images") or {}).get("model") or "gpt-image-2.5-flare"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with Image.open(src) as im:
        im = im.convert("RGB")
        w, h = im.size
        scale = 1600 / max(w, h)
        if scale < 1:
            im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
        im.save(out, "WEBP", quality=82, method=6)  # no EXIF/metadata is carried over
        w, h = im.size
    iptc = False
    if shutil.which("exiftool"):
        res = subprocess.run(["exiftool", "-overwrite_original", f"-XMP-iptcExt:DigitalSourceType={IPTC_URI}", out],
                             capture_output=True, text=True)
        iptc = res.returncode == 0
        if not iptc:
            print("WARNING: exiftool failed:", res.stderr.strip()[:200])
    else:
        print("WARNING: exiftool not on PATH; IPTC DigitalSourceType not written (iptcWritten: false)")
    photos_path = os.path.join(bc.CONTENT, "photos.json")
    with open(photos_path, encoding="utf-8") as f:
        items = json.load(f)
    rel = "/img/blog/ai/" + os.path.basename(out)
    today = datetime.date.today().isoformat()
    entry = {"id": args.id, "file": rel, "shows": args.shows, "room": args.room, "city": None, "materials": [],
             "stage": "detail", "pairWith": None,
             "orientation": "landscape" if w > h else ("portrait" if h > w else "square"),
             "width": w, "height": h, "date": today, "clientConsent": True, "heroOk": args.slot == "hero",
             "source": "ai", "altDefault": args.alt, "prompt": prompt, "model": model, "generatedOn": today,
             "iptcWritten": iptc, "usedIn": []}
    existing = next((x for x in items if x["id"] == args.id), None)
    if existing:
        entry["usedIn"] = existing.get("usedIn", [])
        items[items.index(existing)] = entry
        print(f"photos.json: updated entry '{args.id}'")
    else:
        items.append(entry)
        print(f"photos.json: added entry '{args.id}'")
    with open(photos_path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("written:", rel, f"{w}x{h}", "iptc:", iptc)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prompt-file", help="text file with the full prompt (brief per content/image-style.md)")
    ap.add_argument("--slot", choices=["hero", "body", "diagram"], help="where the image goes")
    ap.add_argument("--size", default="1536x1024", help="WxH accepted by the API (see the OpenAI docs)")
    ap.add_argument("--quality", default="high", help="quality value accepted by the API (see the OpenAI docs)")
    ap.add_argument("--n", type=int, default=3, help="number of candidates (1-3)")
    ap.add_argument("--tmp", required=True, help="folder for the candidates, e.g. /tmp/img-<id>")
    ap.add_argument("--pick", type=int, help="candidate number to keep (switches to step B)")
    ap.add_argument("--id", help="photos.json id, e.g. ai-<slug>-hero")
    ap.add_argument("--out", help="public/img/blog/ai/<name>.webp")
    ap.add_argument("--shows", help="what is visible, factual")
    ap.add_argument("--alt", help="one factual sentence for alt text")
    ap.add_argument("--room", choices=["bath", "shower", "kitchen", "tile", "other"])
    args = ap.parse_args()
    if args.pick:
        pick(args)
    else:
        if not args.prompt_file or not args.slot:
            ap.error("--prompt-file and --slot are required to generate candidates")
        if not 1 <= args.n <= 3:
            ap.error("--n must be 1, 2 or 3")
        generate(args)


if __name__ == "__main__":
    main()
