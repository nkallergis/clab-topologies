"""Module to run NUTS tests from Nautobot."""

import pytest

from nautobot.apps.jobs import Job, register_jobs

name = "AUTOCON3"

class NutJob(Job):
    """A job to run NUTS tests."""

    class Meta:
        """Metadata for the NutJob."""

        name = "NUTS tests"
        description = "A job to run NUTS tests."
        has_sensitive_variables = False

    def run(self, **data):
        """Run NUTS tests."""
        self.logger.info("Running NUTS tests...")
        result = pytest.main(["-q", "--disable-warnings", "tests/*"])
        return result

register_jobs(NutJob)
