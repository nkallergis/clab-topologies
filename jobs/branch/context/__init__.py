"""This module contains the render context for the basic design."""
from netaddr import IPNetwork

from nautobot_design_builder.errors import DesignValidationError
from nautobot_design_builder.context import Context, context_file


@context_file("context.yaml")
class BaseDataContext(Context):
    """Render context for base data."""

@context_file("context.yaml")
class BranchDesignContext(Context):
    """Render context for branch design."""

    @property
    def branch_prefixes(self):
        return {
            "supernet": "10.10.10.0/24"
        }