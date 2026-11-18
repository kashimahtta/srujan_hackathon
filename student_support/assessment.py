"""Apply the transparent concern-point rules to cleaned student data."""

import pandas as pd


SUPPORT_LEVEL_ORDER = ["At risk", "Needs attention", "On track"]


def points(value, low_cut, mid_cut):
    if value < low_cut:
        return 2
    if value < mid_cut:
        return 1
    return 0


def support_level(concern_points):
    if concern_points >= 4:
        return "At risk"
    if concern_points >= 2:
        return "Needs attention"
    return "On track"


def reasons(row):
    signals = []
    if row["attendance_pts"]:
        signals.append(f"attendance {row['attendance_pct']:.0f}%")
    if row["marks_pts"]:
        signals.append(f"internal marks {row['internal_marks']:.0f}")
    if row["assignment_pts"]:
        signals.append(f"assignments {row['assignment_score']:.0f}")
    return ", ".join(signals) if signals else "no concerns"


def assess_students(data):
    """Return rows scored and sorted by the sample support-level rules."""
    assessed = data.copy()
    assessed["attendance_pts"] = assessed["attendance_pct"].apply(
        points, args=(75, 85)
    )
    assessed["marks_pts"] = assessed["internal_marks"].apply(points, args=(50, 60))
    assessed["assignment_pts"] = assessed["assignment_score"].apply(
        points, args=(50, 60)
    )
    assessed["concern_points"] = assessed[
        ["attendance_pts", "marks_pts", "assignment_pts"]
    ].sum(axis=1)
    assessed["support_level"] = assessed["concern_points"].apply(support_level)
    assessed["main_signals"] = assessed.apply(reasons, axis=1)
    assessed["support_level"] = pd.Categorical(
        assessed["support_level"],
        categories=SUPPORT_LEVEL_ORDER,
        ordered=True,
    )
    return assessed.sort_values(
        ["support_level", "concern_points"], ascending=[True, False]
    )
