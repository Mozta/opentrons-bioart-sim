"""
visualization.py — Petri dish visualization for Opentrons Bio-Art protocols
============================================================================
Renders droplet positions, smears, and volume summaries as a matplotlib figure.
"""

from __future__ import annotations

from typing import Optional

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from .colors import PETRI_INNER_DIAMETER


def visualize_petri(
    droplets_x: list[float],
    droplets_y: list[float],
    droplets_size: list[float],
    droplets_color: list[str],
    smears: list[tuple[list[float], list[float], str]],
    total_aspirated: dict[str, float],
    total_dispensed: dict[str, float],
    tip_count: int,
    background: str = 'black',
    title: str = 'Opentrons Bio-Art Simulation',
    save_path: Optional[str] = None,
    show: bool = True,
    dpi: int = 150,
    figsize: tuple[float, float] = (10, 10),
) -> tuple[Figure, Axes]:
    """Render a Petri dish visualization with all dispensed droplets.

    Args:
        droplets_x: X coordinates of each droplet (mm from center).
        droplets_y: Y coordinates of each droplet (mm from center).
        droplets_size: Size of each droplet in scatter points (volume × 100).
        droplets_color: Matplotlib color of each droplet.
        smears: List of (x_list, y_list, color) tuples for smear lines.
        total_aspirated: Dict mapping color name → total µL aspirated.
        total_dispensed: Dict mapping color name → total µL dispensed.
        tip_count: Number of tips used during the protocol.
        background: 'black' (dark agar), 'agar' (beige agar), or 'paper' (outline only).
        title: Plot title.
        save_path: If provided, save figure to this file path.
        show: If True, call plt.show(). Set False for headless/test usage.
        dpi: Resolution for saved images.
        figsize: Figure size in inches.

    Returns:
        Tuple of (Figure, Axes) for further customization.
    """
    # ── Print volume summary ──
    _print_volume_summary(total_aspirated, total_dispensed, tip_count)

    # ── Create figure ──
    fig, ax = plt.subplots(figsize=figsize)

    # ── Petri dish background ──
    radius = PETRI_INNER_DIAMETER / 2
    bg_colors = {
        'black': ('#000000', True),
        'agar':  ('#d7ca95', True),
        'paper': ('#000000', False),
    }
    color, fill = bg_colors.get(background, bg_colors['black'])
    ax.add_patch(plt.Circle((0, 0), radius=radius, color=color, fill=fill))

    # ── Droplets ──
    if droplets_x:
        ax.scatter(droplets_x, droplets_y, droplets_size, c=droplets_color)

    # ── Smears ──
    for xlist, ylist, scolor in smears:
        ax.plot(xlist, ylist, color=scolor, linewidth=4, solid_capstyle='round')

    # ── Axes setup ──
    margin = radius + 0.5
    ax.set_xlim(-margin, margin)
    ax.set_ylim(-margin, margin)
    ax.set_aspect('equal')
    ax.set_title(title)

    # ── Save / Show ──
    if save_path:
        fig.savefig(save_path, dpi=dpi, bbox_inches='tight',
                    facecolor=fig.get_facecolor(), edgecolor='none')
        print(f"\nImage saved to: {save_path}")

    if show:
        plt.show()

    return fig, ax


def _print_volume_summary(
    total_aspirated: dict[str, float],
    total_dispensed: dict[str, float],
    tip_count: int,
) -> None:
    """Print a summary of aspirated/dispensed volumes by color."""
    from .colors import resolve_visual_color

    print("\n=== TOTAL VOLUMES BY COLOR ===")
    all_colors = total_aspirated.keys() | total_dispensed.keys()
    for color in sorted(all_colors):
        asp = total_aspirated.get(color, 0)
        disp = total_dispensed.get(color, 0)
        waste = "\t\t##### WASTE: more aspirated than dispensed!" if asp != disp else ''
        vis = resolve_visual_color(color)
        print(f"\t{color} ({vis}):\t aspirated {asp:.1f}\t dispensed {disp:.1f}{waste}")

    total_asp = sum(total_aspirated.values())
    total_disp = sum(total_dispensed.values())
    print(f"\t[all]:\t\t[aspirated {total_asp:.1f}]\t[dispensed {total_disp:.1f}]")
    print(f"\n=== TIPS USED ===\n\t{tip_count} tip(s)  (ideal: one per color)\n")
