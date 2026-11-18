"""Bounded, count-only ChEMBL activity audit for candidate targets.

No activity pages are downloaded: every request asks for one record and uses
ChEMBL's page_meta.total_count. Unique-compound counts are deliberately not
claimed because they require paginating activity records and local deduplication.
"""

from __future__ import annotations

import csv
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode


OUTPUT = Path(__file__).resolve().parents[1] / "experiment" / "chembl_activity_count_audit.csv"
BASE = "https://www.ebi.ac.uk/chembl/api/data/activity.json"

# Candidate ChEMBL IDs are checked by the API during the query. NMDA and GABA-A
# are intentionally excluded: their requested names do not identify one single
# protein target or one unambiguous docking receptor.
TARGETS = {
    "EGFR": "CHEMBL203",
    "CDK6": "CHEMBL3974",
    "BRAF": "CHEMBL5145",
    "PARP1": "CHEMBL3105",
    "FLT3": "CHEMBL1974",
    "PIK3CA": "CHEMBL4005",
    "JAK3": "CHEMBL2148",
    "TYK2": "CHEMBL3553",
    "JAK1": "CHEMBL2835",
    "IRAK4": "CHEMBL5250",
    "BTK": "CHEMBL5251",
    "DPP4": "CHEMBL284",
    "BACE1": "CHEMBL4822",
    "ACHE": "CHEMBL220",
    "HIV-1 protease": "CHEMBL2366517",
    "SERT": "CHEMBL228",
    "DRD2": "CHEMBL217",
    "NET": "CHEMBL222",
    "OX2R": "CHEMBL5113",
    "GSK3B": "CHEMBL262",
    "SIGMAR1": "CHEMBL287",
}


def count(parameters: dict[str, str]) -> int | None:
    url = f"{BASE}?{urlencode({**parameters, 'limit': '1'})}"
    completed = subprocess.run(
        ["curl.exe", "--connect-timeout", "10", "--max-time", "30", "-sS", url],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        return None
    try:
        return int(json.loads(completed.stdout)["page_meta"]["total_count"])
    except (KeyError, ValueError, json.JSONDecodeError):
        return None


def main() -> None:
    accessed_at = datetime.now(timezone.utc).isoformat()
    rows: list[dict[str, object]] = []
    jobs: list[tuple[str, str, str]] = []
    for symbol, chembl_id in TARGETS.items():
        jobs.append((symbol, chembl_id, "all"))
        jobs.extend((symbol, chembl_id, standard_type) for standard_type in ("IC50", "Ki", "Kd"))

    def one_job(job: tuple[str, str, str]) -> tuple[tuple[str, str, str], int | None]:
        symbol, chembl_id, measure = job
        parameters = {"target_chembl_id": chembl_id}
        if measure != "all":
            parameters.update(
                {
                    "standard_type": measure,
                    "standard_relation": "=",
                    "standard_units": "nM",
                    "standard_value__isnull": "false",
                    "data_validity_comment__isnull": "true",
                }
            )
        return job, count(parameters)

    # Four concurrent read-only requests stay below the recommended five-way
    # independent-call limit and well below ChEMBL's ~10 requests/second guidance.
    counts: dict[tuple[str, str, str], int | None] = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for job, result in pool.map(one_job, jobs):
            counts[job] = result

    for symbol, chembl_id in TARGETS.items():
        total = counts[(symbol, chembl_id, "all")]
        type_counts = {standard_type: counts[(symbol, chembl_id, standard_type)] for standard_type in ("IC50", "Ki", "Kd")}
        strict_sum = None if any(value is None for value in type_counts.values()) else sum(type_counts.values())
        rows.append(
            {
                "target_symbol": symbol,
                "target_chembl_id": chembl_id,
                "all_activity_records": total,
                "strict_ic50_records": type_counts["IC50"],
                "strict_ki_records": type_counts["Ki"],
                "strict_kd_records": type_counts["Kd"],
                "strict_ic50_ki_kd_records_sum": strict_sum,
                "unique_compounds": "not_measured",
                "accessed_at_utc": accessed_at,
                "endpoint": BASE,
                "filter_definition": "standard_type in {IC50,Ki,Kd}; standard_relation '='; standard_units nM; standard_value present; data_validity_comment null",
            }
        )

    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} target rows to {OUTPUT.name}")


if __name__ == "__main__":
    main()
