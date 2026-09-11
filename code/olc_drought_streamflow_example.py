"""Reproduce the OLC drought and low-flow example from prepared public data.

Required input files come from ``2026 Buildathon/data`` in the OLC Climate
Resiliency and Digital Sovereignty Learning Lab repository. They are derived
from manifest-verified NOAA/NCEI and USGS snapshots by that repository's
``prepare_teaching_data.py`` script.

Run from this repository with, for example:

    python code/olc_drought_streamflow_example.py \
      --data-dir "/path/to/Education-Climate-Resiliency-Digital-Sovereignty/2026 Buildathon/data"

Dependencies: numpy, pandas, scipy, matplotlib.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = REPOSITORY_ROOT / "docs" / "assets" / "olc-example"
SOURCE_COMMIT = "a1d5b5b02c4ee23e61213069629087f00794f27f"
EXPECTED_HASHES = {
    "drought_monthly.csv": "c2b400a135daa36631bf35ae0dd0f422b72d8a71d11a023312aff9cbc92dbd00",
    "streamflow_daily.csv": "73a24f5dc5d74173fc4857d42aa68b541e2d7694be9d5a51b50c842af2ffab4c",
}
WHITE_RIVER_GAUGES = {
    "06446000": "White River near Oglala",
    "06446500": "White River near Interior",
    "06447000": "White River near Kadoka",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_inputs(data_dir: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for filename, expected in EXPECTED_HASHES.items():
        path = data_dir / filename
        if not path.is_file():
            raise FileNotFoundError(f"Missing prepared OLC input: {path}")
        actual = sha256(path)
        if actual != expected:
            raise ValueError(
                f"Unexpected contents for {filename}: {actual}. "
                "Re-run the OLC preparation script from the pinned source commit."
            )
        hashes[filename] = actual
    return hashes


def annual_drought(data_dir: Path) -> pd.DataFrame:
    drought = pd.read_csv(data_dir / "drought_monthly.csv", parse_dates=["date"])
    drought["year"] = drought["date"].dt.year
    annual = (
        drought[
            drought["division"].isin([7, 8])
            & drought["year"].between(1990, 2024)
        ]
        .groupby(["division", "year"])
        .agg(pdsi=("pdsi", "mean"), valid_months=("pdsi", "count"))
        .reset_index()
    )
    complete = annual[annual["valid_months"] == 12].pivot(
        index="year", columns="division", values="pdsi"
    )
    complete = complete.dropna(subset=[7, 8])
    result = complete[[7, 8]].mean(axis=1).rename("regional_pdsi").to_frame()
    result["regional_pdsi_z"] = (
        result["regional_pdsi"] - result["regional_pdsi"].mean()
    ) / result["regional_pdsi"].std(ddof=1)
    return result


def annual_low_flow(data_dir: Path) -> pd.DataFrame:
    flow = pd.read_csv(
        data_dir / "streamflow_daily.csv",
        parse_dates=["date"],
        dtype={"site_id": "string"},
    )
    flow = flow[flow["site_id"].isin(WHITE_RIVER_GAUGES)].copy()
    flow["year"] = flow["date"].dt.year

    annual_parts: list[pd.DataFrame] = []
    for site_id, station in WHITE_RIVER_GAUGES.items():
        gauge = flow[flow["site_id"] == site_id].sort_values("date").copy()
        gauge["flow_7day_mean_cfs"] = (
            gauge.set_index("date")["flow_cfs"]
            .rolling("7D", min_periods=7)
            .mean()
            .to_numpy()
        )
        annual = (
            gauge.groupby("year")
            .agg(
                observed_days=("date", "nunique"),
                annual_7day_low_cfs=("flow_7day_mean_cfs", "min"),
            )
            .reset_index()
        )
        annual = annual[annual["observed_days"] >= 330].copy()
        annual["site_id"] = site_id
        annual["station"] = station
        annual_parts.append(annual)

    by_gauge = pd.concat(annual_parts, ignore_index=True)
    by_gauge["low_flow_z"] = by_gauge.groupby("site_id")[
        "annual_7day_low_cfs"
    ].transform(lambda values: (values - values.mean()) / values.std(ddof=1))

    return (
        by_gauge.groupby("year")
        .agg(
            standardized_low_flow=("low_flow_z", "mean"),
            gauges_included=("site_id", "nunique"),
        )
        .query("gauges_included >= 2")
    )


def build_figure(summary: pd.DataFrame, output_path: Path, rho: float) -> None:
    blue = "#234a65"
    green = "#007135"
    red = "#b3473f"
    gray = "#566461"

    fig, axes = plt.subplots(2, 1, figsize=(12, 9))
    fig.subplots_adjust(left=0.1, right=0.97, top=0.9, bottom=0.13, hspace=0.42)
    years = summary.index.to_numpy()

    axes[0].axhline(0, color="#9aa7a2", linewidth=0.8)
    axes[0].plot(
        years,
        summary["regional_pdsi_z"],
        color=red,
        marker="o",
        markersize=3.5,
        linewidth=1.6,
        label="Regional PDSI (standardized)",
    )
    axes[0].plot(
        years,
        summary["standardized_low_flow"],
        color=blue,
        marker="o",
        markersize=3.5,
        linewidth=1.6,
        label="White River annual 7-day low flow (standardized)",
    )
    axes[0].set(
        title="Annual regional drought and low-flow indicators",
        xlabel="Year",
        ylabel="Standardized value\n(lower means drier or lower flow)",
    )
    axes[0].legend(frameon=False, ncol=2, loc="lower center")
    axes[0].grid(axis="y", color="#dfe6e3", linewidth=0.7)

    x = summary["regional_pdsi"].to_numpy()
    y = summary["standardized_low_flow"].to_numpy()
    axes[1].scatter(x, y, color=green, edgecolor="white", linewidth=0.7, s=52)
    slope, intercept = np.polyfit(x, y, 1)
    x_line = np.linspace(x.min(), x.max(), 100)
    axes[1].plot(x_line, intercept + slope * x_line, color=blue, linewidth=1.8)
    axes[1].axvline(0, color="#9aa7a2", linewidth=0.8)
    axes[1].axhline(0, color="#9aa7a2", linewidth=0.8)
    axes[1].set(
        title=f"Drier regional years often aligned with lower-flow years (Spearman ρ = {rho:.2f})",
        xlabel="Equal-weight annual mean PDSI, South Dakota divisions 7 and 8",
        ylabel="Standardized annual 7-day low flow\n(mean across available White River gauges)",
    )
    axes[1].grid(color="#e7ecea", linewidth=0.6)
    fig.text(
        0.1,
        0.052,
        "Sources: NOAA/NCEI PDSI and USGS NWIS prepared OLC snapshots. "
        "1990–2024; complete drought years; ≥330 observed flow days/year; ≥2 gauges/year.",
        color=gray,
        fontsize=9,
    )
    fig.text(
        0.1,
        0.026,
        "Association is not causation or a measure of livestock water availability.",
        color=gray,
        fontsize=9,
    )

    fig.suptitle(
        "When drought reaches the river: public regional indicators move together, imperfectly",
        color=blue,
        fontsize=17,
        fontweight="bold",
    )
    fig.savefig(output_path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    input_hashes = verify_inputs(args.data_dir)
    summary = annual_drought(args.data_dir).join(annual_low_flow(args.data_dir), how="inner")
    if len(summary) != 35 or summary.index.min() != 1990 or summary.index.max() != 2024:
        raise ValueError("Unexpected analysis coverage; inspect the prepared source snapshots.")

    spearman = stats.spearmanr(summary["regional_pdsi"], summary["standardized_low_flow"])
    pearson = stats.pearsonr(summary["regional_pdsi"], summary["standardized_low_flow"])

    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary.round(6).to_csv(args.output_dir / "drought_streamflow_summary.csv", index_label="year")
    build_figure(summary, args.output_dir / "drought_streamflow_relationship.png", float(spearman.statistic))

    metrics = {
        "source_curriculum": "OLC Climate Resiliency and Digital Sovereignty Learning Lab",
        "source_repository": "https://github.com/olc-techsupport/Education-Climate-Resiliency-Digital-Sovereignty",
        "source_commit": SOURCE_COMMIT,
        "prepared_input_sha256": input_hashes,
        "period": [1990, 2024],
        "years_compared": int(len(summary)),
        "drought_measure": "equal-weight annual mean PDSI for South Dakota climate divisions 7 and 8; both divisions require 12 valid months",
        "flow_measure": "annual minimum of rolling seven-day mean daily discharge, standardized within each White River gauge",
        "flow_gauges": WHITE_RIVER_GAUGES,
        "flow_completeness": "at least 330 observed days per station-year and at least two included gauges per year",
        "spearman_rho": round(float(spearman.statistic), 6),
        "pearson_r": round(float(pearson.statistic), 6),
        "interpretation": "Drier regional years often coincided with lower-flow years, but the relationship was imperfect.",
        "limitations": [
            "The comparison is observational and does not establish causation.",
            "Climate divisions and gauges do not represent every place, water source, or use.",
            "Standardization makes gauges comparable but removes their absolute-flow scale.",
            "The rolling seven-day window may cross calendar-year boundaries.",
            "The data do not directly measure livestock water availability, water quality, infrastructure, or community impacts.",
        ],
    }
    (args.output_dir / "analysis_metrics.json").write_text(
        json.dumps(metrics, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(metrics, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
