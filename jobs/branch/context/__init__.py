"""This module contains the render context for the basic design."""
from netaddr import IPNetwork

from nautobot_design_builder.errors import DesignValidationError
from nautobot_design_builder.context import Context, context_file
from nautobot.ipam.models import Prefix

@context_file("context.yaml")
class BaseDataContext(Context):
    """Render context for base data."""

@context_file("context.yaml")
class BranchDesignContext(Context):
    """Render context for branch design."""

    @property
    def branch_prefixes(self):
        """Calculate the branch prefixes."""
        try:
            supernet = Prefix.objects.get(location=self.site_name, role__name="Branch:Supernet")
        except:
            supernet = "1.2.3.0/24"
        return {
            "supernet": supernet,
        }