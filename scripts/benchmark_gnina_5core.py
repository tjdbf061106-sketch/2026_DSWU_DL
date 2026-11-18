"""Run one reproducible CPU-only GNINA docking benchmark and record wall time."""

from __future__ import annotations

import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = PROJECT_DIR.parent
EXPERIMENT_DIR = PROJECT_DIR / "experiment"
IMAGE = "gnina/gnina:v1.3.3"
PROTEIN = WORKSPACE_DIR / "protein.pdb"
LIGAND = WORKSPACE_DIR / "ligand.sdf"
SEED = 20261118


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, text=True, capture_output=True)


def main() -> None:
    if not PROTEIN.is_file() or not LIGAND.is_file():
        raise FileNotFoundError("protein.pdb and ligand.sdf are required in the workspace root")
    EXPERIMENT_DIR.mkdir(exist_ok=True)
    run(["docker", "image", "inspect", IMAGE])

    pose_output = EXPERIMENT_DIR / "benchmark_gnina_5core_pose.sdf"
    stdout_path = EXPERIMENT_DIR / "benchmark_gnina_5core_stdout.log"
    stderr_path = EXPERIMENT_DIR / "benchmark_gnina_5core_stderr.log"
    pose_output.unlink(missing_ok=True)

    mount = f"type=bind,src={WORKSPACE_DIR},dst=/data"
    command = [
        "docker", "run", "--pull=never", "--rm", "--cpus=5", "--mount", mount,
        IMAGE, "gnina",
        "-r", "/data/protein.pdb",
        "-l", "/data/ligand.sdf",
        "--autobox_ligand", "/data/ligand.sdf",
        "--cpu", "5",
        "--no_gpu",
        "--exhaustiveness", "8",
        "--seed", str(SEED),
        "--out", "/data/deep_learning_final_project/experiment/benchmark_gnina_5core_pose.sdf",
    ]
    started = time.perf_counter()
    completed = subprocess.run(command, text=True, capture_output=True)
    elapsed = time.perf_counter() - started
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")

    metadata = {
        "benchmark_id": "gnina_cpu_5core_single_ligand",
        "measured_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "completed" if completed.returncode == 0 else "failed",
        "model": {"tool": "GNINA", "docker_image": IMAGE},
        "hardware_constraint": {
            "device": "CPU",
            "docker_cpu_limit": 5,
            "gnina_cpu_argument": 5,
            "gpu_disabled": True,
        },
        "input": {
            "protein": PROTEIN.name,
            "ligand": LIGAND.name,
            "ligand_count": 1,
            "search_box": "autobox_ligand from the provided ligand",
            "exhaustiveness": 8,
            "random_seed": SEED,
        },
        "measurement": {
            "wall_clock_seconds_for_one_ligand": elapsed,
            "wall_clock_minutes_for_one_ligand": elapsed / 60,
            "return_code": completed.returncode,
            "note": "This is a single-ligand CPU docking measurement, not a throughput estimate for arbitrary compounds.",
        },
        "outputs": {
            "docked_pose": pose_output.name if pose_output.exists() else None,
            "stdout_log": stdout_path.name,
            "stderr_log": stderr_path.name,
        },
    }
    metadata_path = EXPERIMENT_DIR / "benchmark_gnina_5core_metadata.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
