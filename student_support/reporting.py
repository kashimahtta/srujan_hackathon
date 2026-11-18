"""Console summaries, CSV export, and visualizations for the sample data."""

from io import BytesIO

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from student_support.assessment import SUPPORT_LEVEL_ORDER
from student_support.data import MEASURES


COLORS = {
    "On track": "#4C9F70",
    "Needs attention": "#E9A23B",
    "At risk": "#D95D5D",
}

FOLLOW_UP_ACTIONS = {
    "On track": "Keep encouraging; share positive feedback; offer extension tasks.",
    "Needs attention": (
        "Friendly check-in; ask what would help; point to resources "
        "(notes, practice sets, peer study groups)."
    ),
    "At risk": (
        "Private, supportive one-to-one conversation; explore barriers together; "
        "agree a small action plan; involve counselling/tutoring if the student wants it."
    ),
}


def print_raw_preview(data):
    print("SAMPLE DATA -- first 5 rows (raw)")
    print(data.head(), "\n")


def print_data_quality(data):
    print("Missing values before cleaning:\n", data[MEASURES].isna().sum(), "\n")
    print("Duplicate rows:", data.duplicated().sum())
    invalid_count = int(
        ((data[MEASURES] > 100) | (data[MEASURES] < 0)).sum().sum()
    )
    print("Values outside 0-100:", invalid_count, "\n")


def print_exploration(data):
    print("Summary statistics:\n", data[MEASURES].describe().round(1), "\n")
    print("Correlation between measures:\n", data[MEASURES].corr().round(2), "\n")


def print_student_results(data):
    print(
        "Students per support level:\n",
        data["support_level"].value_counts().reindex(SUPPORT_LEVEL_ORDER),
        "\n",
    )
    print("Students who may benefit from a supportive check-in (sample data):")
    columns = [
        "student_id",
        "attendance_pct",
        "internal_marks",
        "assignment_score",
        "concern_points",
        "support_level",
        "main_signals",
    ]
    print(
        data[data["support_level"] != "On track"][columns].to_string(index=False)
    )


def create_chart(data, data_label="SAMPLE DATA"):
    """Render the chart as bytes for web responses and file exports."""
    counts = data["support_level"].value_counts().reindex(SUPPORT_LEVEL_ORDER)
    figure, axes = plt.subplots(1, 2, figsize=(13, 5))

    axes[0].bar(
        counts.index.astype(str),
        counts.values,
        color=[COLORS[level] for level in counts.index],
    )
    axes[0].set_title(f"Students by support level ({data_label})")
    axes[0].set_ylabel("Number of students")
    for index, count in enumerate(counts.values):
        axes[0].text(index, count + 0.3, str(count), ha="center")

    for level in SUPPORT_LEVEL_ORDER:
        subset = data[data["support_level"] == level]
        axes[1].scatter(
            subset["attendance_pct"],
            subset["internal_marks"],
            s=40 + subset["assignment_score"],
            alpha=0.75,
            color=COLORS[level],
            label=level,
            edgecolor="white",
        )
    axes[1].axvline(75, ls="--", color="grey", lw=0.8)
    axes[1].axhline(50, ls="--", color="grey", lw=0.8)
    axes[1].set_xlabel("Attendance (%)")
    axes[1].set_ylabel("Internal marks")
    axes[1].set_title("Attendance vs internal marks\n(dot size = assignment score)")
    axes[1].legend()

    figure.suptitle(
        f"Early support indicator -- {data_label.lower()}, not validated predictions",
        fontsize=11,
        y=1.0,
    )
    figure.tight_layout()
    image = BytesIO()
    figure.savefig(image, format="png", dpi=150, bbox_inches="tight")
    plt.close(figure)
    image.seek(0)
    return image


def save_chart(data, output_path="student_support_chart.png"):
    image = create_chart(data)
    with open(output_path, "wb") as output_file:
        output_file.write(image.getvalue())


def print_follow_up_actions():
    print("\nSuggested follow-up:")
    for level in SUPPORT_LEVEL_ORDER:
        print(f"  {level}: {FOLLOW_UP_ACTIONS[level]}")


def save_results(data):
    print_student_results(data)
    data.to_csv("student_support_results.csv", index=False)
    save_chart(data)
    print_follow_up_actions()
