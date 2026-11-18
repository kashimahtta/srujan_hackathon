# Student Support Indicator

A classroom demonstration that generates invented student data, applies transparent
rule-based support levels, and displays results in a Flask dashboard.

The project helps demonstrate how attendance, internal marks, and assignment scores
can highlight opportunities for a supportive student check-in. It provides
explanations and suggested follow-up actions alongside charts and summary counts.

> **Educational demonstration only:** the included dataset is invented and the
> thresholds are assumptions, not validated predictions. Do not upload real student
> data or identifying information, and do not use the results to make decisions
> about a student.

## Features

- View an automatically generated sample class and its support-level summary.
- Analyze one anonymous record using the form, or multiple records using CSV upload.
- Review concern points, signals, a chart, and suggested supportive actions.
- Run the original command-line version to export a CSV report and chart.

## Tools and technologies

| Technology | Purpose |
| --- | --- |
| Python | Application and data-processing language |
| Flask and Jinja | Web routes, form handling, and HTML templates |
| pandas | Data cleaning, tabular analysis, and CSV processing |
| NumPy | Reproducible sample-data generation |
| Matplotlib | Support-level and attendance charts |
| HTML and CSS | Dashboard layout and styling |
| GitHub Actions | Automated tests with Python 3.11 and 3.12 |
| Vercel | Flask deployment |

## How the indicator works

Each measure contributes concern points. These cutoffs are examples only:

| Measure | 2 points | 1 point | 0 points |
| --- | --- | --- | --- |
| Attendance (%) | Below 75 | 75 to below 85 | 85 or above |
| Internal marks | Below 50 | 50 to below 60 | 60 or above |
| Assignment score | Below 50 | 50 to below 60 | 60 or above |

The total determines the sample support level: **On track** (0–1 points),
**Needs attention** (2–3 points), or **At risk** (4–6 points).

## Project structure

```text
.
├── app.py                         # Flask entry point for Vercel
├── public/
│   └── style.css                  # Static stylesheet served by Vercel
├── student_support/
│   ├── assessment.py              # Concern points and support levels
│   ├── data.py                    # Sample-data generation and cleaning
│   ├── reporting.py               # Console output, CSV, and chart
│   ├── service.py                 # Shared data-to-results pipeline
│   ├── web.py                     # Flask routes and input validation
│   └── templates/
│       └── index.html             # Dashboard and input forms
├── tests/
│   └── test_student_support.py
├── student_support_project.py     # Command-line entry point
├── requirements.txt
└── vercel.json
```

## Run locally

You need Python and pip installed. Git is needed if you clone the repository.
Python 3.11 and 3.12 are tested in GitHub Actions.

1. Clone the project and open its folder:

```bash
git clone https://github.com/kashimahtta/srujan_hackathon.git
cd srujan_hackathon
```

If you already have the project files, open a terminal in the project folder instead.

2. Create and activate a virtual environment:

**Windows PowerShell**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Start the dashboard:

```bash
python -m flask --app app run
```

5. Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.
   Stop the server with `Ctrl+C`.

## Enter data

Use the manual form for one anonymous record, or upload a UTF-8 CSV with exactly
these columns in this order:

```csv
student_id,attendance_pct,internal_marks,assignment_score
demo-001,72,48,55
demo-002,90,80,85
```

Each ID must be non-empty and no longer than 40 characters. All three measures
must be numeric values from 0 to 100. CSV requests are limited to 2 MB. Submitted
data is processed for that response only and is not saved by the application;
refreshing the page returns to the generated sample.

## Command-line report

With the same dependencies installed, run:

```bash
python student_support_project.py
```

It writes `student_support_results.csv` and `student_support_chart.png` in the
current directory.

## Deploy to Vercel

1. Push this project to a GitHub repository.
2. Import the repository in Vercel and keep the repository root as the project root.
3. Vercel detects the Flask application in `app.py` and installs dependencies from
   `requirements.txt`.
4. Deploy.

## Tests

```bash
python -m unittest discover -s tests
```

GitHub Actions runs this test command on pushes and pull requests.

## Copyright

Copyright © 2026 Kashi Mahtta — Code Hacker Team.
