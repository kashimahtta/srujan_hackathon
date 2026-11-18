"""Shared pipeline for building the assessed sample results."""

from student_support.assessment import assess_students
from student_support.data import clean_data, create_sample_data


def build_results(data=None):
    """Create, clean, and assess data, or assess a supplied raw data frame."""
    if data is None:
        data = create_sample_data()
    return assess_students(clean_data(data))
