"""Flask dashboard for local and Vercel deployment."""

import base64
from pathlib import Path

import pandas as pd
from flask import Flask, render_template, request, send_file

from student_support.assessment import SUPPORT_LEVEL_ORDER
from student_support.reporting import FOLLOW_UP_ACTIONS, create_chart
from student_support.service import build_results


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024
PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"
REQUIRED_COLUMNS = [
    "student_id",
    "attendance_pct",
    "internal_marks",
    "assignment_score",
]


def _dashboard(results=None, error=None, submitted=False, status=200):
    counts = {}
    students = []
    chart_data = None

    if results is not None:
        counts = (
            results["support_level"]
            .value_counts()
            .reindex(SUPPORT_LEVEL_ORDER, fill_value=0)
            .to_dict()
        )
        columns = REQUIRED_COLUMNS + [
            "concern_points",
            "support_level",
            "main_signals",
            "data_check_needed",
        ]
        check_ins = results[results["support_level"] != "On track"][columns]
        students = check_ins.to_dict(orient="records")
        data_label = "USER-SUBMITTED DATA" if submitted else "SAMPLE DATA"
        chart_data = base64.b64encode(
            create_chart(results, data_label=data_label).getvalue()
        ).decode("ascii")

    return (
        render_template(
            "index.html",
            counts=counts,
            students=students,
            actions=FOLLOW_UP_ACTIONS,
            total_students=0 if results is None else len(results),
            chart_data=chart_data,
            error=error,
            submitted=submitted,
        ),
        status,
    )


def _validated_numeric_columns(data):
    for column in REQUIRED_COLUMNS[1:]:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    if data[REQUIRED_COLUMNS[1:]].isna().any().any():
        raise ValueError("All three measures must be valid numbers.")
    if not data[REQUIRED_COLUMNS[1:]].ge(0).all().all():
        raise ValueError("Measures must be between 0 and 100.")
    if not data[REQUIRED_COLUMNS[1:]].le(100).all().all():
        raise ValueError("Measures must be between 0 and 100.")
    if data["student_id"].isna().any() or data["student_id"].astype(str).str.strip().eq("").any():
        raise ValueError("Every row needs a non-empty anonymous ID.")
    data["student_id"] = data["student_id"].astype(str).str.strip()
    if data["student_id"].str.len().gt(40).any():
        raise ValueError("Anonymous IDs must be 40 characters or fewer.")
    return data


def _manual_input(form):
    data = pd.DataFrame([{
        "student_id": form.get("student_id", "").strip(),
        "attendance_pct": form.get("attendance_pct", ""),
        "internal_marks": form.get("internal_marks", ""),
        "assignment_score": form.get("assignment_score", ""),
    }])
    return _validated_numeric_columns(data)


def _csv_input(upload):
    if upload is None or not upload.filename:
        raise ValueError("Choose a CSV file to upload.")
    try:
        data = pd.read_csv(upload, encoding="utf-8-sig")
    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError):
        raise ValueError("The uploaded file could not be read as a CSV.") from None
    if data.empty:
        raise ValueError("The CSV must contain at least one student row.")
    if list(data.columns) != REQUIRED_COLUMNS:
        expected = ", ".join(REQUIRED_COLUMNS)
        raise ValueError(f"CSV columns must be exactly: {expected}.")
    return _validated_numeric_columns(data)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return _dashboard(build_results())

    try:
        input_type = request.form.get("input_type")
        if input_type == "manual":
            data = _manual_input(request.form)
        elif input_type == "csv":
            data = _csv_input(request.files.get("csv_file"))
        else:
            raise ValueError("Choose manual entry or CSV upload.")
        return _dashboard(build_results(data), submitted=True)
    except ValueError as error:
        return _dashboard(error=str(error), status=400)


@app.errorhandler(413)
def request_too_large(_error):
    return _dashboard(
        error="The uploaded request is too large. CSV uploads are limited to 2 MB.",
        status=413,
    )


@app.route("/style.css")
def stylesheet():
    return send_file(PUBLIC_DIR / "style.css", mimetype="text/css")
