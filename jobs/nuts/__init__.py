"""Module to run NUTS tests from Nautobot."""

import io
import json
import sys
from pathlib import Path

import pytest

from nautobot.apps.jobs import Job, ObjectVar, register_jobs

from containerlab.models import Topology

name = "AUTOCON3"  # pylint: disable=invalid-name


class NutJob(Job):
    """A job to run NUTS tests."""

    topology = ObjectVar(
        description="The topology to use for the tests.",
        model=Topology,
        required=True,
    )

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
                    "-p",
                    "no:all",
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
            report_data = report_path.read_text()
            self.create_file("nuts_report.json", report_data)
            full_report = json.loads(report_data)
            report = {
                "created": full_report.get("created"),
                "duration": full_report.get("duration"),
                "exitcode": full_report.get("exitcode"),
                "summary": full_report.get("summary"),
                "result": {},
            }
            for result in ["error", "failed", "passed"]:
                report["result"][result] = [
                    test.get("nodeid") for test in full_report.get("tests") if test.get("outcome") == result
                ]
            return report
        self.logger.error("Report was not generated!")
        return {}


register_jobs(NutJob)
