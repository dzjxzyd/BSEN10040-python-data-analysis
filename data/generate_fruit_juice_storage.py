"""Generate a deterministic synthetic fruit-juice storage dataset.

The numbers in this module are for classroom demonstration only.  They are
constructed to make common data-analysis operations easy to see; they are not
measurements of real juice or food-safety evidence.
"""

from pathlib import Path

import numpy as np
import pandas as pd


COLUMNS = [
    "sample_id",
    "juice_type",
    "storage_temp_C",
    "storage_day",
    "batch",
    "vitamin_c_mg_per_100ml",
    "pH",
    "microbial_load_log10",
    "turbidity_NTU",
]

JUICE_TYPES = ("orange", "apple", "berry")
STORAGE_TEMPERATURES_C = (4, 20, 35)
STORAGE_DAYS = (0, 2, 4, 6)
BATCHES = (1, 2, 3)

JUICE_VITAMIN_C_BASELINES = {"orange": 52.0, "apple": 44.0, "berry": 36.0}
JUICE_PH_BASELINES = {"orange": 3.65, "apple": 3.82, "berry": 3.35}
JUICE_MICROBIAL_LOAD_BASELINES = {
    "orange": 1.85,
    "apple": 1.75,
    "berry": 2.05,
}
JUICE_TURBIDITY_OFFSETS_NTU = {"orange": 0.0, "apple": 1.5, "berry": 3.0}

VITAMIN_C_DAY_DECAY = 0.70
VITAMIN_C_TEMPERATURE_DECAY = 0.025
PH_DAY_DECAY = 0.006
PH_TEMPERATURE_DAY_DECAY = 0.0008
MICROBIAL_LOAD_DAY_GROWTH = 0.09
MICROBIAL_LOAD_TEMPERATURE_DAY_GROWTH = 0.018
TURBIDITY_BASELINE_NTU = 4.0
TURBIDITY_MICROBIAL_LOAD_SLOPE = 4.5

VITAMIN_C_NOISE_SD = 0.35
PH_NOISE_SD = 0.025
MICROBIAL_LOAD_NOISE_SD = 0.07
TURBIDITY_NOISE_SD = 0.7

TEACHING_MISSING_PH_SAMPLE_IDS = ("S011", "S071")
TEACHING_MISSING_TURBIDITY_SAMPLE_IDS = ("S026", "S091")
TEACHING_OUTLIER_SAMPLE_ID = "S108"
TEACHING_OUTLIER_MICROBIAL_LOAD = 7.8


def _calculate_turbidity(juice_type, microbial_load, noise):
    """Calculate turbidity from juice type, microbial load and measurement noise."""

    return round(
        TURBIDITY_BASELINE_NTU
        + JUICE_TURBIDITY_OFFSETS_NTU[juice_type]
        + TURBIDITY_MICROBIAL_LOAD_SLOPE * microbial_load
        + noise,
        1,
    )


def build_dataset(seed=42):
    """Return a reproducible synthetic fruit-juice storage experiment.

    The design contains every combination of juice type, temperature, day and
    batch.  Small random measurement errors keep the example realistic enough
    for teaching while leaving the intended trends visible.
    """

    rng = np.random.default_rng(seed)
    records = []
    turbidity_noise_by_sample_id = {}
    sample_number = 1

    for juice_type in JUICE_TYPES:
        for temperature in STORAGE_TEMPERATURES_C:
            for day in STORAGE_DAYS:
                for batch in BATCHES:
                    # The formulas deliberately make the main classroom
                    # patterns stronger than the small simulated noise.
                    vitamin_c = (
                        JUICE_VITAMIN_C_BASELINES[juice_type]
                        - day
                        * (
                            VITAMIN_C_DAY_DECAY
                            + VITAMIN_C_TEMPERATURE_DECAY * (temperature - 4)
                        )
                        + rng.normal(0, VITAMIN_C_NOISE_SD)
                    )
                    ph = (
                        JUICE_PH_BASELINES[juice_type]
                        - PH_DAY_DECAY * day
                        - PH_TEMPERATURE_DAY_DECAY * (temperature - 4) * day
                        + rng.normal(0, PH_NOISE_SD)
                    )
                    microbial_load = (
                        JUICE_MICROBIAL_LOAD_BASELINES[juice_type]
                        + MICROBIAL_LOAD_DAY_GROWTH * day
                        + MICROBIAL_LOAD_TEMPERATURE_DAY_GROWTH
                        * (temperature - 4)
                        * day
                        + rng.normal(0, MICROBIAL_LOAD_NOISE_SD)
                    )
                    sample_id = f"S{sample_number:03d}"
                    turbidity_noise = rng.normal(0, TURBIDITY_NOISE_SD)
                    turbidity_noise_by_sample_id[sample_id] = turbidity_noise
                    turbidity = _calculate_turbidity(
                        juice_type, microbial_load, turbidity_noise
                    )
                    records.append(
                        {
                            "sample_id": sample_id,
                            "juice_type": juice_type,
                            "storage_temp_C": temperature,
                            "storage_day": day,
                            "batch": batch,
                            "vitamin_c_mg_per_100ml": round(vitamin_c, 2),
                            "pH": round(ph, 2),
                            "microbial_load_log10": round(microbial_load, 2),
                            "turbidity_NTU": round(turbidity, 1),
                        }
                    )
                    sample_number += 1

    df = pd.DataFrame(records, columns=COLUMNS)

    # Deliberate teaching values, located by stable sample IDs rather than row positions.
    df.loc[df["sample_id"].isin(TEACHING_MISSING_PH_SAMPLE_IDS), "pH"] = np.nan
    df.loc[
        df["sample_id"].isin(TEACHING_MISSING_TURBIDITY_SAMPLE_IDS), "turbidity_NTU"
    ] = np.nan

    outlier_mask = df["sample_id"].eq(TEACHING_OUTLIER_SAMPLE_ID)
    df.loc[outlier_mask, "microbial_load_log10"] = TEACHING_OUTLIER_MICROBIAL_LOAD
    outlier_juice_type = df.loc[outlier_mask, "juice_type"].iloc[0]
    df.loc[outlier_mask, "turbidity_NTU"] = _calculate_turbidity(
        outlier_juice_type,
        TEACHING_OUTLIER_MICROBIAL_LOAD,
        turbidity_noise_by_sample_id[TEACHING_OUTLIER_SAMPLE_ID],
    )

    return df


def write_dataset(path, seed=42):
    """Write :func:`build_dataset` to *path* as a CSV file."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    build_dataset(seed=seed).to_csv(output_path, index=False)


if __name__ == "__main__":
    output_path = Path(__file__).with_name("fruit_juice_storage.csv")
    write_dataset(output_path)
    print(f"Wrote synthetic dataset to {output_path}")
