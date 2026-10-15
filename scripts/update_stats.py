"""Generate a local SVG from public GitHub data. Python standard library only."""

import json
import os
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
USERNAME = os.environ.get("PROFILE_USERNAME", "AnkjoD")


def fetch(path):
    headers = {"User-Agent": "AnkjoD-profile", "Accept": "application/vnd.github+json"}
    token = os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    request = Request("https://api.github.com" + path, headers=headers)
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def main():
    user_path = "/users/" + quote(USERNAME, safe="")
    user = fetch(user_path)
    repos = []
    page = 1
    while True:
        batch = fetch(f"{user_path}/repos?type=owner&per_page=100&page={page}")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    originals = [repo for repo in repos if not repo["fork"] and not repo.get("private", False)]
    metrics = [
        (len(repos), "KHO CÔNG KHAI"),
        (sum(repo["stargazers_count"] for repo in originals), "SAO NHẬN ĐƯỢC"),
        (sum(repo["forks_count"] for repo in originals), "LƯỢT FORK"),
        (user["followers"], "NGƯỜI THEO DÕI"),
    ]
    stamp = datetime.now(timezone.utc).strftime("%d/%m/%Y · %H:%M UTC")
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="960" height="132" viewBox="0 0 960 132" role="img" aria-labelledby="title desc">',
        f'<title id="title">Thống kê công khai của {escape(USERNAME)}</title>',
        '<desc id="desc">' + escape("; ".join(f"{label}: {value}" for value, label in metrics)) + f'. Cập nhật {stamp}.</desc>',
        '<rect x="1" y="1" width="958" height="130" rx="14" fill="#100d18" stroke="#33263f"/>',
        '<g font-family="Segoe UI,DejaVu Sans,Arial,sans-serif">',
    ]
    for index, (value, label) in enumerate(metrics):
        x = 30 + 234 * index
        color = "#eab4c8" if index in (1, 3) else "#c3a5ee"
        parts.append(f'<text x="{x}" y="62" fill="{color}" font-size="38" font-weight="600">{value:,}</text>')
        parts.append(f'<text x="{x}" y="99" fill="#c4bacf" font-size="12" letter-spacing="1">{label}</text>')
        if index < 3:
            parts.append(f'<path d="M{x + 207} 24V108" stroke="#33263f"/>')
    parts.append('</g></svg>')
    destination = ROOT / "assets" / "stats-card.svg"
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".tmp")
    temporary.write_text("\n".join(parts), encoding="utf-8")
    temporary.replace(destination)
    print(f"Updated public stats for {USERNAME}")


if __name__ == "__main__":
    main()
