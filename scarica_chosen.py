#!/usr/bin/env python3
"""The Chosen: catalogo pubblico, video 1080p H.264 e solo audio italiano.
Python 3.10+; FFmpeg nel PATH. Senza --scarica verifica soltanto il catalogo.
"""
import argparse
import csv
import json
from pathlib import Path
import re
import shutil
import subprocess
import urllib.request
from urllib.parse import urljoin


def get(url, structured=True):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        body = response.read().decode("utf-8-sig")
    return json.loads(body) if structured else body


def attributes(line):
    return {m[0]: m[1] if m[1] else m[2] for m in
            re.findall(r'([\w-]+)=(?:"([^"]*)"|([^,]*))', line)}


def streams(master):
    lines = get(master, False).splitlines()
    audio, video = [], []
    for i, line in enumerate(lines):
        attrs = attributes(line)
        if line.startswith("#EXT-X-MEDIA:") and attrs.get("TYPE") == "AUDIO":
            if attrs.get("LANGUAGE", "").lower().split("-")[0] in ("it", "ita"):
                audio.append(attrs)
        if line.startswith("#EXT-X-STREAM-INF:"):
            if attrs.get("RESOLUTION") == "1920x1080" and "avc1" in attrs.get("CODECS", ""):
                uri = next((s for s in lines[i+1:] if s and not s.startswith("#")), None)
                if uri:
                    video.append((attrs, urljoin(master, uri)))
    for attrs, video_url in sorted(video, key=lambda v: int(v[0].get("BANDWIDTH", 0)), reverse=True):
        for track in audio:
            if track.get("GROUP-ID") == attrs.get("AUDIO") and track.get("URI"):
                return video_url, urljoin(master, track["URI"])
    raise ValueError("1080p H.264 con audio italiano non disponibile")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scarica", action="store_true", help="Avvia i download; altrimenti verifica soltanto")
    parser.add_argument("--stagioni", nargs="+", type=int, help="Esempio: --stagioni 1 2; predefinito: tutte quelle disponibili")
    parser.add_argument("--cartella", type=Path, default=Path(__file__).resolve().parent / "Filmati")
    parser.add_argument("--limite", type=int, help="Numero massimo di episodi da verificare/scaricare")
    args = parser.parse_args()
    if args.scarica and not shutil.which("ffmpeg"):
        parser.error("FFmpeg non trovato nel PATH")
    args.cartella.mkdir(parents=True, exist_ok=True)
    cards = get("https://api.watch.thechosen.tv/v1/seasons")["data"]["seasonCards"]
    rows, seen = [], set()
    for card in cards:
        slug = card.get("cta", {}).get("href", "")
        match = re.fullmatch(r"season-(\d+)", slug)
        if not match or not card.get("episodeCount") or card.get("isLocked"):
            continue
        season = int(match[1])
        if args.stagioni and season not in args.stagioni:
            continue
        page = get(f"https://api.watch.thechosen.tv/v2/pages/by/{slug}?locale=en")
        # Solo la raccolta Episodes: evita trailer, aftershow e tavole rotonde.
        sections = [s for s in page["data"]["sections"] if s.get("displayTitle") == "Episodes"]
        if not sections:
            raise ValueError(f"Raccolta Episodes non trovata: {slug}")
        items = [item for section in sections for item in section.get("playlist", {}).get("items", [])]
        if not items:
            raise ValueError(f"Catalogo episodi vuoto: {slug}")
        for item in items:
            video = item.get("video", {})
            identifier = str(video.get("videoID", ""))
            if not identifier or identifier in seen:
                continue
            if args.limite and len(seen) >= args.limite:
                break
            seen.add(identifier)
            title = video.get("title", identifier)
            row = {"stagione": season, "titolo": title, "id": identifier, "stato": "", "file": ""}
            try:
                metadata = get(f"https://api.watch.thechosen.tv/v1/videos/{identifier}")
                if metadata.get("isLocked"):
                    raise ValueError("Episodio bloccato")
                sources = metadata.get("details", {}).get("video", [])
                master = next(s["url"] for s in sources if s.get("type") == "hls")
                video_url, audio_url = streams(master)
                episode = metadata.get("episodeNumber")
                label = f"S{season:02d}E{int(episode):02d}" if episode is not None else f"S{season:02d}_{identifier}"
                folder = args.cartella / f"Stagione {season:02d}"
                target = folder / f"The Chosen - {label} - {identifier} - ITA 1080p.mp4"
                row["file"] = str(target)
                row["stato"] = "DISPONIBILE: 1080p + italiano"
                if args.scarica:
                    folder.mkdir(exist_ok=True)
                    if target.exists():
                        row["stato"] = "GIA PRESENTE (saltato, non riverificato)"
                    else:
                        partial = target.with_suffix(".incompleto.mp4")
                        subprocess.run([
                            "ffmpeg", "-hide_banner", "-nostdin", "-y",
                            "-i", video_url, "-i", audio_url,
                            "-map", "0:v:0", "-map", "1:a:0", "-c", "copy",
                            "-metadata:s:a:0", "language=ita", "-movflags", "+faststart", str(partial)
                        ], check=True)
                        partial.replace(target)
                        row["stato"] = "SCARICATO"
            except Exception as error:
                row["stato"] = f"ERRORE: {error}"
            rows.append(row)
            print(f"{title}: {row['stato']}", flush=True)
    report = args.cartella / "verifica.csv"
    with report.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["stagione", "titolo", "id", "stato", "file"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nEpisodi esaminati: {len(rows)}. Resoconto: {report}")
    if not rows or any(r["stato"].startswith("ERRORE") for r in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
