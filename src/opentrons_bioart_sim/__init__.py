"""
opentrons-bioart-sim — Local simulator & visualizer for Opentrons OT-2 bio-art protocols
=========================================================================================

Run and visualize HTGAA / Opentrons Art Designer protocols without physical hardware.

Quick start::

    from opentrons_bioart_sim import OpentronsMock, simulate_protocol

    # Option A — one-liner
    mock = simulate_protocol('my_protocol.py')

    # Option B — manual control
    mock = OpentronsMock(well_colors)
    run(mock)
    mock.visualize(background='black', save_path='output.png')
"""

__version__ = "1.0.0"

from .colors import PROTEIN_VISUAL_COLORS, resolve_visual_color  # noqa: F401
from .mock import OpentronsMock, simulate_protocol  # noqa: F401

__all__ = [
    "OpentronsMock",
    "simulate_protocol",
    "resolve_visual_color",
    "PROTEIN_VISUAL_COLORS",
    "__version__",
]
