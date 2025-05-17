"""This module contains the render context for the basic design."""

from django.core.exceptions import ObjectDoesNotExist
from netaddr import IPNetwork

from nautobot_design_builder.errors import DesignValidationError
from nautobot_design_builder.context import Context, context_file
from nautobot.dcim.models import Location
from nautobot.ipam.models import Prefix

@context_file("context.yaml")
class BaseDataContext(Context):
    """Render context for base data."""

@context_file("context.yaml")
class BranchDesignContext(Context):
    """Render context for branch design."""

    def get_next_prefix(self):
        """Get next available prefix."""
        return "1.2.3.0/24"

    @property
    def branch_prefixes(self):
        """Calculate the branch prefixes."""
        try:
            location = Location.objects.get(name=self.site_name)
            supernet = Prefix.objects.get(location=location, role__name="Branch:Supernet")
        except ObjectDoesNotExist:
            supernet = self.get_next_prefix()
        return {
            "supernet": supernet,
        }