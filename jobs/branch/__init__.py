"""Basic design demonstrates the capabilities of the Design Builder."""
from nautobot.apps.jobs import register_jobs, StringVar, IPNetworkVar, ObjectVar

from nautobot.dcim.models import Location

from nautobot_design_builder.contrib import ext
from nautobot_design_builder.design_job import DesignJob

from .context import BaseDataContext, BranchDesignContext

class BaseData(DesignJob):
    """Load base data."""

    class Meta:
        """Metadata for the BaseData design."""

        name = "Base Data"
        nautobot_version = ">=2"
        has_sensitive_variables = False
        design_file = "designs/0000_basedata.yaml.j2"
        context_class = BaseDataContext

class BranchDesign(DesignJob):
    """A basic design for design builder."""

    region = ObjectVar(
        label="Region",
        description="Region for the new branch",
        model=Location,
    )

    site_name = StringVar(label="Site Name", regex=r"\w{3}\d+")
    site_prefix = IPNetworkVar(label="Site Prefix")

    class Meta:
        """Metadata describing this design job."""

        name = "Branch Design"
        nautobot_version = ">=2"
        has_sensitive_variables = False
        extensions = [ext.CableConnectionExtension]
        design_file = "designs/0001_branchdesign.yaml.j2"
        context_class = BranchDesignContext

name = "Demo Designs"
register_jobs(BaseData, BranchDesign)