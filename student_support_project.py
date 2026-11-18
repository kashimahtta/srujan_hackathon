"""
Early Academic Support Indicator -- classroom demonstration
============================================================
All data in this project is SAMPLE DATA invented for teaching purposes.
No real students are represented. Results are NOT validated predictions.

Requires: pandas, numpy, matplotlib
Run:      python student_support_project.py
"""

from student_support.assessment import assess_students
from student_support.data import clean_data, create_sample_data
from student_support.reporting import (
    print_data_quality,
    print_exploration,
    print_raw_preview,
    save_results,
)


def main():
    raw_data = create_sample_data()
    print_raw_preview(raw_data)
    print_data_quality(raw_data)

    cleaned_data = clean_data(raw_data)
    print_exploration(cleaned_data)

    results = assess_students(cleaned_data)
    save_results(results)


if __name__ == "__main__":
    main()
