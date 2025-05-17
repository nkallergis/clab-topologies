"""This module contains the render context for the basic design."""
from nautobot_design_builder.context import Context, context_file


class BaseDataContext(Context):
    """Render context for base data."""

@context_file("context.yaml")
class BranchDesignContext(Context):
    """Render context for branch design."""
