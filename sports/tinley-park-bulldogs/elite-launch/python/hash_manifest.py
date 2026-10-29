#!/usr/bin/env python3
import argparse, hashlib, json, subprocess
from pathlib import Path

VIDEO_EXTS={".mov",".mp4",".m4v"}

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(4*1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def ffprobe(path):
    cmd=[
      "ffprobe","-v","quiet","-print_format","json",
      "-show_entries","format=duration:format_tags=com.apple.quicktime.creationdate",
      "-show_entries","stream=codec_type,width,height,avg_frame_rate",
      str(path)
    ]
    return json.loads(subprocess.check_output(cmd))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--out",default="video_manifest.json")
    args=ap.parse_args()
    rows=[]
    for p in sorted(Path(args.folder).iterdir()):
        if p.suffix.lower() not in VIDEO_EXTS: continue
        rows.append({
          "filename":p.name,
          "sha256":sha256_file(p),
          "bytes":p.stat().st_size,
          "probe":ffprobe(p),
          "review_status":"UNREVIEWED",
          "evidence_label":"VERIFIED"
        })
    Path(args.out).write_text(json.dumps(rows,indent=2))
    print(f"Wrote {len(rows)} assets")
if __name__=="__main__": main()
