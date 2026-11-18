"""Measure CPU-only ADMET-AI throughput on a ChEMBL SMILES sample.

The script intentionally constrains this process to five logical CPUs and
writes only measured timing data plus predictions from the benchmark sample.
It does not claim that projected values are full-library results.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Set before importing NumPy/PyTorch through pandas or ADMET-AI.
for variable in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[variable] = "1"

import pandas as pd
import psutil
import torch
from admet_ai import ADMETModel


DEFAULT_INPUT = Path(r"C:\Users\DS\DL\chembl_37_id_smiles\smiles.csv")
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[1] / "experiment"


def configure_utf8_console() -> None:
    """Avoid Windows legacy-console failures from Lightning/Rich progress text."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def count_data_rows(path: Path) -> int:
    """Count CSV rows without retaining the library in memory."""
    with path.open("rb") as handle:
        return max(0, sum(1 for _ in handle) - 1)


def configure_five_cores() -> list[int]:
    """Constrain the benchmark process and all child workers to five CPUs."""
    process = psutil.Process()
    available = process.cpu_affinity()
    if len(available) < 5:
        raise RuntimeError(f"Only {len(available)} logical CPUs are available; five are required.")
    selected = available[:5]
    process.cpu_affinity(selected)
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    return selected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--rows", type=int, default=10_000)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    if args.rows <= 0:
        raise ValueError("--rows must be positive")
    if not args.input.is_file():
        raise FileNotFoundError(args.input)

    configure_utf8_console()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    affinity = configure_five_cores()
    started = time.perf_counter()
    source_rows = count_data_rows(args.input)
    sample = pd.read_csv(args.input, nrows=args.rows)
    read_seconds = time.perf_counter() - started

    model_start = time.perf_counter()
    model = ADMETModel(include_physchem=False, drugbank_path=None, num_workers=5)
    model_load_seconds = time.perf_counter() - model_start

    unique_smiles = sample["smiles"].dropna().drop_duplicates().tolist()
    prediction_start = time.perf_counter()
    predictions = model.predict(smiles=unique_smiles)
    prediction_seconds = time.perf_counter() - prediction_start

    result = sample.join(predictions, on="smiles")
    prediction_columns = [column for column in predictions.columns if column != "smiles"]
    predicted_rows = int(result[prediction_columns].notna().any(axis=1).sum())
    invalid_or_unpredicted_rows = int(len(sample) - predicted_rows)
    output_csv = args.output_dir / "benchmark_admet_5core_predictions.csv"
    output_csv.unlink(missing_ok=True)
    result.to_csv(output_csv, index=False)

    throughput = predicted_rows / prediction_seconds if prediction_seconds else None
    estimated_full_prediction_seconds = source_rows / throughput if throughput else None
    metadata = {
        "benchmark_id": "admet_ai_cpu_5core",
        "status": "completed",
        "measured_at_utc": datetime.now(timezone.utc).isoformat(),
        "model": {
            "name": "ADMET-AI bundled pretrained ensembles",
            "package_version": importlib.metadata.version("admet-ai"),
            "include_physchem": False,
            "dataloader_num_workers": 5,
        },
        "hardware_constraint": {
            "device": "CPU",
            "cpu_affinity_logical_ids": affinity,
            "cpu_affinity_count": len(affinity),
            "torch_num_threads": torch.get_num_threads(),
            "torch_num_interop_threads": torch.get_num_interop_threads(),
            "blas_thread_environment": {
                variable: os.environ[variable]
                for variable in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS")
            },
            "host_logical_cpus": psutil.cpu_count(logical=True),
            "host_physical_cpus": psutil.cpu_count(logical=False),
            "platform": platform.platform(),
        },
        "input": {
            "filename": args.input.name,
            "full_library_rows": source_rows,
            "benchmark_input_rows": len(sample),
            "unique_nonempty_smiles": len(unique_smiles),
        },
        "measurement": {
            "read_and_row_count_seconds": read_seconds,
            "model_load_seconds": model_load_seconds,
            "prediction_seconds": prediction_seconds,
            "total_elapsed_seconds": time.perf_counter() - started,
            "predicted_rows": predicted_rows,
            "invalid_or_unpredicted_rows": invalid_or_unpredicted_rows,
            "throughput_predicted_rows_per_second": throughput,
            "full_library_prediction_estimate_seconds": estimated_full_prediction_seconds,
            "full_library_prediction_estimate_hours": (
                estimated_full_prediction_seconds / 3600 if estimated_full_prediction_seconds else None
            ),
            "projection_note": "Projection is a linear estimate from one 10,000-row CPU benchmark; it excludes interruptions and may change with molecule complexity.",
        },
        "outputs": {"benchmark_predictions": output_csv.name},
    }
    metadata_path = args.output_dir / "benchmark_admet_5core_metadata.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
