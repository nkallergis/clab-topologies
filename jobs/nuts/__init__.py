"""Module to run NUTS tests from Nautobot."""

import io
import json
import sys
from pathlib import Path

import pytest

from nautobot.apps.jobs import Job, register_jobs

name = "AUTOCON3"   # pylint: disable=invalid-name

class NutJob(Job):
    """A job to run NUTS tests."""

    class Meta:
        """Metadata for the NutJob."""

        name = "NUTS Tests"
        description = "A job to run NUTS tests."
        has_sensitive_variables = False

    def run(self, **data):  # pylint: disable=arguments-differ
        """Run NUTS tests."""
        self.logger.info("Running NUTS tests...")
        
        # Set up the paths
        pwd = Path(__file__).parent
        tests_path = pwd / "tests"
        report_path = pwd / ".report.json"
        if report_path.exists():
            report_path.unlink()

        # Temporarily disable stdout and stderr to avoid cluttering the Nautobot logs
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()

        try:
            # Run the tests
            pytest.main(
                [
                    tests_path,
                    "-p", "no:all",
                    "--json-report",
                    f"--json-report-file={report_path}",
                ]
            )
        finally:
            # Restore stdout and stderr
            sys.stdout = original_stdout
            sys.stderr = original_stderr

        # Read the result, return the report
        if report_path.exists():
            report = json.loads(report_path.read_text())
            self.create_file("report.json", report)
            return report["summary"]
        self.logger.error("Report file was not generated!")
        return {}


register_jobs(NutJob)
