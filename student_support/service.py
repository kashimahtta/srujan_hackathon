"""Shared pipeline for building the assessed sample results."""

from pathlib import Path

import pandas as pd

from student_support.assessment import SUPPORT_LEVEL_ORDER, assess_students
from student_support.data import clean_data


DEMO_RESULTS_PATH = Path(__file__).with_name("demo_results.csv")


def build_results(data=None):
    """Load the demo results or clean and assess supplied raw data."""
    if data is None:
        results = pd.read_csv(DEMO_RESULTS_PATH)
        if not results["support_level"].isin(SUPPORT_LEVEL_ORDER).all():
            raise ValueError("The demo CSV contains an unknown support level.")
        results["support_level"] = pd.Categorical(
            results["support_level"], categories=SUPPORT_LEVEL_ORDER, ordered=True
        )
        return results
    return assess_students(clean_data(data))
