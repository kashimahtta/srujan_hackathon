"""Create and clean the invented classroom sample data."""

import numpy as np
import pandas as pd


MEASURES = ["attendance_pct", "internal_marks", "assignment_score"]


def create_sample_data():
    """Return reproducible, invented student data with a few data issues."""
    rng = np.random.default_rng(seed=42)
    student_count = 40
    engagement = rng.normal(0, 1, student_count)

    data = pd.DataFrame({
        "student_id": [f"S{i:03d}" for i in range(1, student_count + 1)],
        "attendance_pct": np.clip(
            80 + 10 * engagement + rng.normal(0, 5, student_count), 40, 100
        ).round(1),
        "internal_marks": np.clip(
            65 + 12 * engagement + rng.normal(0, 7, student_count), 15, 100
        ).round(1),
        "assignment_score": np.clip(
            68 + 13 * engagement + rng.normal(0, 8, student_count), 10, 100
        ).round(1),
    })

    data.loc[5, "attendance_pct"] = np.nan
    data.loc[12, "internal_marks"] = np.nan
    data.loc[20, "assignment_score"] = 105.0
    return pd.concat([data, data.iloc[[8]]], ignore_index=True)


def clean_data(data):
    """Remove duplicate rows and impute invalid or missing measures."""
    cleaned = data.drop_duplicates().reset_index(drop=True).copy()

    for column in MEASURES:
        cleaned.loc[(cleaned[column] < 0) | (cleaned[column] > 100), column] = np.nan

    cleaned["data_check_needed"] = cleaned[MEASURES].isna().any(axis=1)
    for column in MEASURES:
        cleaned[column] = cleaned[column].fillna(cleaned[column].median())

    return cleaned
