"""Module to run NUTS tests from Nautobot."""

import json
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
        report_path = pwd / "report.json"
        if report_path.exists():
            report_path.unlink()
        
        # Run the tests
        # result = pytest.main(["-q", "--disable-warnings", pwd / "tests"])
        result = pytest.main(
            [
                tests_path,
                "--json-report",
                f"--json-report-file={report_path}",
                "-p",
                "no:terminal",
            ]
        )

        # Read the result, return the report
        if report_path.exists():
            report = json.loads(report_path.read_text())
            return result, report
        else:
            self.logger.error("Report file was not generated!")
            return result, {}


register_jobs(NutJob)
