"""Basic design demonstrates the capabilities of the Design Builder."""
from nautobot.apps.jobs import register_jobs, StringVar, IPNetworkVar, ObjectVar

from nautobot.dcim.models import Location

from nautobot_design_builder.contrib import ext
from nautobot_design_builder.design_job import DesignJob

from .context import BranchDesignContext

class BaseData(DesignJob):
    """Load base data."""

    class Meta:
        """Metadata for the BaseData design."""

        name = "Base Data"
        design_file = "designs/0000_design.yaml.j2"
        nautobot_version = ">=2"

class BranchDesign(DesignJob):
    """A basic design for design builder."""

    region = ObjectVar(
        label="Region",
        description="Region for the new branch",
        model=Location,
    )

    site_name = StringVar(label="Site Name", regex=r"\w{3}\d+")
    site_prefix = IPNetworkVar(label="Site Prefix")
    has_sensitive_variables = False

    class Meta:
        """Metadata describing this design job."""

        name = "Branch Design"
        commit_default = False
        design_file = "designs/0001_design.yaml.j2"
        context_class = BranchDesignContext
        nautobot_version = ">=2"
        extensions = [ext.CableConnectionExtension]

name = "Demo Designs"
register_jobs(BaseData, BranchDesign)