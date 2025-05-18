"""Module to run NUTS tests from Nautobot."""

import pytest
from pathlib import Path

from nautobot.apps.jobs import Job, register_jobs

name = "AUTOCON3"

class NutJob(Job):
    """A job to run NUTS tests."""

    class Meta:
        """Metadata for the NutJob."""

        name = "NUTS Tests"
        description = "A job to run NUTS tests."
        has_sensitive_variables = False

    def run(self, **data):
        """Run NUTS tests."""
        self.logger.info("Running NUTS tests...")
        
        pwd = Path(__file__).parent
        log_level = self.logger.level
        self.logger.setLevel("ERROR")
        result = pytest.main(["-q", "--disable-warnings", pwd / "tests"])
        self.logger.setLevel(log_level)
        return result

register_jobs(NutJob)
