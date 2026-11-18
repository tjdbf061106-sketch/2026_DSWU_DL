"""Portable count-only ChEMBL and RCSB audit; Python 3.11+ stdlib only."""
from __future__ import annotations
import csv, json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

OUT = Path(__file__).parent / "results"
TARGETS = {"EGFR":"CHEMBL203","CDK6":"CHEMBL3974","BRAF":"CHEMBL5145","PARP1":"CHEMBL3105","FLT3":"CHEMBL1974","PIK3CA":"CHEMBL4005","JAK3":"CHEMBL2148","TYK2":"CHEMBL3553","JAK1":"CHEMBL2835","IRAK4":"CHEMBL5250","BTK":"CHEMBL5251","DPP4":"CHEMBL284","BACE1":"CHEMBL4822","ACHE":"CHEMBL220","HIV-1 protease":"CHEMBL2366517","SERT":"CHEMBL228","DRD2":"CHEMBL217","NET":"CHEMBL222","OX2R":"CHEMBL5113","GSK3B":"CHEMBL262","SIGMAR1":"CHEMBL287"}
PDB = {"BACE1":"4DJW","DPP4":"1X70","PARP1":"4UND","BTK":"5P9J","TYK2":"4GIH"}

def get(url):
    try:
        with urlopen(Request(url, headers={"Accept":"application/json","User-Agent":"DSWU-target-audit/1.0"}), timeout=30) as r: return json.load(r)
    except Exception: return None

def count(target, kind):
    p={"target_chembl_id":target,"limit":"1"}
    if kind != "all": p.update({"standard_type":kind,"standard_relation":"=","standard_units":"nM","standard_value__isnull":"false","data_validity_comment__isnull":"true"})
    d=get("https://www.ebi.ac.uk/chembl/api/data/activity.json?"+urlencode(p))
    return d.get("page_meta",{}).get("total_count","not_measured") if d else "not_measured"

def target_row(item):
    name, tid=item; v={k:count(tid,k) for k in ("all","IC50","Ki","Kd")}; a=[v[x] for x in ("IC50","Ki","Kd")]
    return {"target":name,"target_chembl_id":tid,"all_activity_records":v["all"],"strict_ic50":v["IC50"],"strict_ki":v["Ki"],"strict_kd":v["Kd"],"strict_sum":sum(a) if all(isinstance(x,int) for x in a) else "not_measured","unique_compounds":"not_measured"}

def pdb_row(item):
    target,pid=item; d=get(f"https://data.rcsb.org/rest/v1/core/entry/{pid}"); info=d.get("rcsb_entry_info",{}) if d else {}; exp=d.get("exptl",[{}]) if d else [{}]
    return {"target":target,"pdb_id":pid,"status":"verified" if d else "not_measured","method":exp[0].get("method"),"resolution":';'.join(map(str,info.get("resolution_combined",[]))),"nonpolymer_entity_count":info.get("nonpolymer_entity_count")}

def write(path, rows):
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def main():
    OUT.mkdir(exist_ok=True); stamp=datetime.now(timezone.utc).isoformat()
    with ThreadPoolExecutor(max_workers=4) as p: targets=list(p.map(target_row,TARGETS.items()))
    with ThreadPoolExecutor(max_workers=5) as p: structures=list(p.map(pdb_row,PDB.items()))
    for row in targets+structures: row["accessed_at_utc"]=stamp
    write(OUT/"chembl_activity_counts.csv",targets); write(OUT/"rcsb_structures.csv",structures)
    (OUT/"provenance.json").write_text(json.dumps({"accessed_at_utc":stamp,"strict_filter":"IC50/Ki/Kd; =; nM; value present; validity comment null","unique_compounds":"not measured"},indent=2),encoding="utf-8")
    print("Wrote results/chembl_activity_counts.csv and results/rcsb_structures.csv")
if __name__ == "__main__": main()
