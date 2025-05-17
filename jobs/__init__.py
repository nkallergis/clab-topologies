"""The __init__.py module is required for Nautobot to load the jobs via Git."""

from .branch import BaseData, BranchDesign

__all__ = [
    "BaseData",
    "BranchDesign",
]