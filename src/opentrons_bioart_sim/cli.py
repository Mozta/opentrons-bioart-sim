"""
cli.py — Command-line interface for opentrons-bioart-sim
========================================================

Usage::

    opentrons-bioart-sim my_protocol.py
    opentrons-bioart-sim my_protocol.py --background agar --save output.png
    opentrons-bioart-sim my_protocol.py --no-show --verbose
"""

from __future__ import annotations

import argparse
import sys

from . import __version__


def main(argv: list[str] | None = None) -> None:
    """Main entry point for the opentrons-bioart-sim CLI."""
    parser = argparse.ArgumentParser(
        prog="opentrons-bioart-sim",
        description="Simulate and visualize Opentrons OT-2 bio-art protocols locally.",
        epilog=(
            "Examples:\n"
            "  opentrons-bioart-sim my_design.py\n"
            "  opentrons-bioart-sim my_design.py --background agar\n"
            "  opentrons-bioart-sim my_design.py --save output.png --no-show\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "protocol",
        help="Path to the protocol .py file (must contain a run(protocol) function)",
    )
    parser.add_argument(
        "--background",
        choices=["black", "agar", "paper"],
        default="black",
        help="Petri dish background style (default: black)",
    )
    parser.add_argument(
        "--save",
        metavar="PATH",
        default=None,
        help="Save the visualization to an image file (e.g. output.png)",
    )
    parser.add_argument(
        "--title",
        default="Opentrons Bio-Art Simulation",
        help="Title for the visualization plot",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Don't display the plot window (useful for headless/CI environments)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=150,
        help="Resolution for saved images (default: 150)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print debug messages for each robot operation",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    args = parser.parse_args(argv)

    from .mock import simulate_protocol

    print(f"Simulating protocol: {args.protocol}")
    print(f"Petri dish background: {args.background}")
    print(f"{'─' * 50}")

    try:
        simulate_protocol(
            protocol_file_path=args.protocol,
            background=args.background,
            save_path=args.save,
            title=args.title,
            show=not args.no_show,
            dpi=args.dpi,
            verbose=args.verbose,
        )
    except FileNotFoundError:
        print(f"Error: File not found: '{args.protocol}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error running protocol: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\n{'─' * 50}")
    print("Simulation completed")


if __name__ == "__main__":
    main()
