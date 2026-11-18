from io import BytesIO
import unittest

from student_support.assessment import assess_students
from student_support.data import clean_data, create_sample_data
from student_support.web import app


class StudentSupportTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_sample_data_is_cleaned_and_assessed(self):
        raw_data = create_sample_data()
        self.assertEqual(len(raw_data), 41)

        cleaned = clean_data(raw_data)
        self.assertEqual(len(cleaned), 40)
        self.assertTrue(cleaned["data_check_needed"].any())
        measures = ["attendance_pct", "internal_marks", "assignment_score"]
        self.assertTrue(cleaned[measures].ge(0).all().all())
        self.assertTrue(cleaned[measures].le(100).all().all())

        assessed = assess_students(cleaned)
        self.assertIn("support_level", assessed.columns)
        self.assertIn("main_signals", assessed.columns)

    def test_dashboard_shows_sample_results(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Demonstration only", response.data)
        self.assertIn(b"data:image/png;base64", response.data)

    def test_manual_submission_is_validated_and_not_persisted(self):
        response = self.client.post(
            "/",
            data={
                "input_type": "manual",
                "student_id": "demo-001",
                "attendance_pct": "40",
                "internal_marks": "30",
                "assignment_score": "35",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"demo-001", response.data)
        self.assertIn(b"Results below are based only on the data submitted", response.data)

        later_response = self.client.get("/")
        self.assertNotIn(b"demo-001", later_response.data)

    def test_csv_submission_and_invalid_values(self):
        response = self.client.post(
            "/",
            data={
                "input_type": "csv",
                "csv_file": (
                    BytesIO(
                        b"student_id,attendance_pct,internal_marks,assignment_score\n"
                        b"csv-001,45,35,40\n"
                    ),
                    "students.csv",
                ),
            },
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"csv-001", response.data)

        invalid_response = self.client.post(
            "/",
            data={
                "input_type": "manual",
                "student_id": "bad-001",
                "attendance_pct": "101",
                "internal_marks": "50",
                "assignment_score": "50",
            },
        )
        self.assertEqual(invalid_response.status_code, 400)
        self.assertIn(b"Measures must be between 0 and 100", invalid_response.data)


if __name__ == "__main__":
    unittest.main()
