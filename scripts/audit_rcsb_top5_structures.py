"""Verify representative ligand-containing PDB entries for five candidates."""

from __future__ import annotations

import csv
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path


OUTPUT = Path(__file__).resolve().parents[1] / "experiment" / "rcsb_top5_structure_audit.csv"
ENTRIES = {
    "BACE1": "4DJW",
    "DPP4": "1X70",
    "PARP1": "4UND",
    "BTK": "5P9J",
    "TYK2": "4GIH",
}


def retrieve(item: tuple[str, str]) -> dict[str, object]:
    target, pdb_id = item
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    response = subprocess.run(
        ["curl.exe", "--connect-timeout", "10", "--max-time", "30", "-sS", url],
        text=True,
        capture_output=True,
        check=False,
    )
    if response.returncode:
        return {"target": target, "pdb_id": pdb_id, "status": "request_failed"}
    try:
        data = json.loads(response.stdout)
    except json.JSONDecodeError:
        return {"target": target, "pdb_id": pdb_id, "status": "unparseable"}
    info = data.get("rcsb_entry_info", {})
    return {
        "target": target,
        "pdb_id": pdb_id,
        "status": "verified",
        "experimental_method": data.get("exptl", [{}])[0].get("method", "") if data.get("exptl") else "",
        "resolution_angstrom": "; ".join(str(value) for value in info.get("resolution_combined", [])),
        "nonpolymer_entity_count": info.get("nonpolymer_entity_count"),
        "title": data.get("struct", {}).get("title"),
        "endpoint": url,
    }


def main() -> None:
    with ThreadPoolExecutor(max_workers=5) as pool:
        rows = list(pool.map(retrieve, ENTRIES.items()))
    accessed = datetime.now(timezone.utc).isoformat()
    for row in rows:
        row["accessed_at_utc"] = accessed
    fields = [
        "target", "pdb_id", "status", "experimental_method", "resolution_angstrom",
        "nonpolymer_entity_count", "title", "endpoint", "accessed_at_utc",
    ]
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} structure rows to {OUTPUT.name}")


if __name__ == "__main__":
    main()
