"""
mock.py — Mock classes simulating the Opentrons OT-2 Python API
================================================================
Provides drop-in replacements for ProtocolContext, InstrumentContext (pipette),
Labware, Well, and hardware modules, enabling protocol testing and visualization
without physical hardware.
"""

from __future__ import annotations

import warnings
from typing import Optional

from opentrons import types

from .colors import MAX_DRAW_RADIUS, resolve_visual_color
from .visualization import visualize_petri


# ═══════════════════════════════════════════════════════════════════════
# Internal helpers
# ═══════════════════════════════════════════════════════════════════════

_null_location = types.Location(types.Point(x=250, y=250, z=250), None)


def _mock_print(msg: str, verbose: bool = False) -> None:
    """Print debug message when verbose mode is enabled."""
    if verbose:
        print("... " + msg)


def _same_2d_location(loc1: types.Location, loc2: types.Location) -> bool:
    """Compare two locations ignoring Z (only X, Y, and labware)."""
    return (
        loc1.point.x == loc2.point.x
        and loc1.point.y == loc2.point.y
        and loc1.labware == loc2.labware
    )


# ═══════════════════════════════════════════════════════════════════════
# WellMock — Simulates an individual well
# ═══════════════════════════════════════════════════════════════════════

class WellMock:
    """Simulates an Opentrons Well.

    Each well has an ID (e.g. 'A1') and an associated color representing
    the fluorescent protein or reagent it contains.
    """

    def __init__(self, well_id: str, well_color: str, labware_official_name: object) -> None:
        self.well_id = well_id
        self.labware_official_name = labware_official_name
        self.well_color = well_color if well_color else 'purple'

    def get_row_col(self) -> tuple[int, int]:
        """Return (row_ordinal, column_number) for this well."""
        row = ord(self.well_id[0].upper())
        col = int(self.well_id[1:])
        return (row, col)

    def set_row_col(self, row: int, col: int) -> None:
        """Set the well ID from row ordinal and column number."""
        self.well_id = chr(row) + str(col)

    def color(self) -> str:
        """Return the raw color/protein name associated with this well."""
        return self.well_color

    def visual_color(self) -> str:
        """Return the resolved matplotlib color for this well's protein."""
        return resolve_visual_color(self.well_color)

    def bottom(self, z: float = 0) -> WellMock:
        """Simulate Well.bottom() — returns self for chaining."""
        assert z >= 0
        return self

    def center(self) -> WellMock:
        """Simulate Well.center() — returns self for chaining."""
        return self

    def top(self, z: float = 0) -> types.Location:
        """Simulate Well.top() — returns a Location at the top of the well."""
        assert isinstance(z, (int, float))
        return types.Location(types.Point(x=0, y=0, z=z), 'Well')

    def move(self, location: types.Location) -> WellMock:
        """Simulate Well.move() — returns self for chaining."""
        assert isinstance(location, types.Location)
        return self

    def __eq__(self, other: object) -> bool:
        return self.__class__ == other.__class__ and self.__dict__ == other.__dict__

    def __repr__(self) -> str:
        return self.well_id


# ═══════════════════════════════════════════════════════════════════════
# LabwareMock — Simulates labware (plates, tip racks, etc.)
# ═══════════════════════════════════════════════════════════════════════

class LabwareMock:
    """Simulates an Opentrons Labware (well plates, tip racks, custom plates)."""

    def __init__(
        self,
        labware_official_name: str,
        deck_slot: int,
        display_name: str,
        well_colors: dict[str, str],
        verbose: bool = False,
    ) -> None:
        self.labware_official_name = labware_official_name
        self.deck_slot = deck_slot
        self.display_name = display_name
        self.well_colors = well_colors
        self.verbose = verbose

    def well(self, well_id: str) -> WellMock:
        """Return a WellMock for the given well ID."""
        return WellMock(well_id, self.well_colors.get(well_id, ''), self)

    def wells(self) -> list[WellMock]:
        """Return a list of all WellMock objects in this labware."""
        return [self.well(wid) for wid in self.well_colors]

    def set_offset(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        """No-op in simulation — on the real robot this adjusts calibration offset."""
        _mock_print(f"set_offset(x={x}, y={y}, z={z}) on {self.display_name}",
                    self.verbose)

    def __getitem__(self, well_id: str) -> WellMock:
        return WellMock(well_id, self.well_colors.get(well_id, ''), self)

    def __repr__(self) -> str:
        return f"Deck Slot {self.deck_slot} - {self.display_name}"


# ═══════════════════════════════════════════════════════════════════════
# ModuleMock — Simulates hardware modules (temperature, thermocycler)
# ═══════════════════════════════════════════════════════════════════════

class ModuleMock:
    """Simulates an Opentrons hardware module (Temperature Module, Thermocycler)."""

    def __init__(
        self,
        module_official_name: str,
        deck_slot: int,
        well_colors: dict[str, str],
        verbose: bool = False,
    ) -> None:
        self.module_official_name = module_official_name
        self.deck_slot = deck_slot
        self.well_colors = well_colors
        self.verbose = verbose

    def load_labware(self, labware_official_name: str, display_name: str = "") -> LabwareMock:
        """Load labware onto this module."""
        _mock_print(f"Module {self.module_official_name} loaded {labware_official_name}",
                    self.verbose)
        return LabwareMock(labware_official_name, self.deck_slot, display_name,
                          self.well_colors, self.verbose)

    def set_temperature(self, celsius: int | float) -> None:
        """Set the module temperature."""
        assert isinstance(celsius, (int, float)) and 4 <= celsius <= 110
        _mock_print(f"Setting temperature to {celsius}°C", self.verbose)

    def open_lid(self) -> None:
        _mock_print("Opening lid", self.verbose)

    def close_lid(self) -> None:
        _mock_print("Closing lid", self.verbose)

    def set_lid_temperature(self, temperature: int | float) -> None:
        assert isinstance(temperature, (int, float)) and 4 <= temperature <= 110
        _mock_print(f"Setting lid temperature to {temperature}°C", self.verbose)

    def deactivate_lid(self) -> None:
        _mock_print("Deactivate lid", self.verbose)

    def set_block_temperature(
        self,
        temperature: int | float,
        hold_time_minutes: int = 0,
        hold_time_seconds: int = 0,
        ramp_rate: float = 0,
        block_max_volume: int = 25,
    ) -> None:
        assert isinstance(temperature, (int, float)) and 4 <= temperature <= 110
        _mock_print(f"Setting block temperature to {temperature}°C", self.verbose)
        if hold_time_minutes > 0:
            _mock_print(f"Holding for {hold_time_minutes} minutes...", self.verbose)
        if hold_time_seconds > 0:
            _mock_print(f"Holding for {hold_time_seconds} seconds...", self.verbose)

    def execute_profile(
        self,
        steps: list[dict],
        repetitions: int,
        block_max_volume: int,
    ) -> None:
        assert isinstance(repetitions, int) and isinstance(block_max_volume, int)
        _mock_print(f"Executing protocol for {repetitions} cycles", self.verbose)
        for step in steps:
            assert isinstance(step, dict)
            _mock_print(f"  Temperature: {step['temperature']}°C, Time: {step['hold_time_seconds']}s",
                        self.verbose)


# ═══════════════════════════════════════════════════════════════════════
# PipetteSim — Simulates the pipette and records droplets
# ═══════════════════════════════════════════════════════════════════════

class PipetteSim:
    """Simulates InstrumentContext (p20_single_gen2 pipette).

    Tracks every dispense as a droplet for final Petri dish visualization.
    Records positions, volumes, colors, and smear movements.
    """

    def __init__(
        self,
        instrument_official_name: str,
        mount_LR: str,
        tip_rack_list: list[LabwareMock],
        well_colors: dict[str, str],
        verbose: bool = False,
    ) -> None:
        if instrument_official_name != "p20_single_gen2":
            raise ValueError(
                f"Unsupported pipette: {instrument_official_name} — must be p20_single_gen2"
            )
        self.max_volume = 20
        self.instrument_official_name = instrument_official_name

        if mount_LR != "right":
            raise ValueError(f"Unsupported mount: {mount_LR} — must be 'right'")
        self.mount_LR = mount_LR

        if tip_rack_list[0].labware_official_name != "opentrons_96_tiprack_20ul":
            raise ValueError(
                f"Unsupported tip rack: {tip_rack_list[0].labware_official_name}"
                " — must be opentrons_96_tiprack_20ul"
            )
        self.tip_rack_list = tip_rack_list
        self.well_colors = well_colors
        self.starting_tip: Optional[WellMock] = None
        self.verbose = verbose

        # Droplet tracking state
        self.droplets_x: list[float] = []
        self.droplets_y: list[float] = []
        self.droplets_size: list[float] = []
        self.droplets_color: list[str] = []
        self.smears: list[tuple[list[float], list[float], str]] = []

        # Pipette state
        self.location: types.Location = _null_location
        self.justDispensedAt: Optional[types.Location] = None
        self.current_volume: float = 0
        self.aspirated_loc: object = None
        self.totalAspirated: dict[str, float] = {}
        self.totalDispensed: dict[str, float] = {}
        self.curr_color: str = 'orange'
        self.has_tip: bool = False
        self.tip_count: int = 0

    def __del__(self) -> None:
        if getattr(self, 'has_tip', False):
            warnings.warn(
                "Protocol ended without dropping the tip (drop_tip)!",
                RuntimeWarning,
                stacklevel=2,
            )

    def _get_last_location_by_api_version(self) -> types.Location:
        return self.location

    def petriLocOfWell(self, well: WellMock) -> types.Location:
        """Map a Well to a position on the Petri dish diagram."""
        assert isinstance(well, WellMock)
        x, y = well.get_row_col()
        return well.top().move(types.Point(
            x=(x - ord('D')) * MAX_DRAW_RADIUS / 4,
            y=(y - 6) * MAX_DRAW_RADIUS / 6,
            z=0,
        ))

    def smearIfJustDispensed(self, loc: types.Location | WellMock) -> None:
        """Draw a smear if the pipette moves immediately after dispensing."""
        assert isinstance(loc, (types.Location, WellMock))
        if self.justDispensedAt is not None:
            newloc = loc if isinstance(loc, types.Location) else self.petriLocOfWell(loc)
            if not _same_2d_location(self.justDispensedAt, newloc):
                line_end = self.justDispensedAt.move(
                    0.5 * (newloc.point - self.justDispensedAt.point)
                )
                self.smears.append((
                    [self.justDispensedAt.point.x, line_end.point.x],
                    [self.justDispensedAt.point.y, line_end.point.y],
                    resolve_visual_color(self.curr_color),
                ))
        self.justDispensedAt = None

    # ──── Opentrons API methods ────

    def dispense(self, volume: float, location: types.Location) -> None:
        """Dispense liquid at the given location.

        Records the droplet position, size, and color for visualization.

        Args:
            volume: Volume in µL to dispense.
            location: Target location (must be a types.Location, not a Well).

        Raises:
            AssertionError: If location is not a types.Location.
            RuntimeError: If no tip is attached.
            ValueError: If volume exceeds current volume, is non-positive,
                        or target is outside the safe draw area.
        """
        assert isinstance(location, types.Location), \
            "dispense() requires a types.Location — not a Well or TrashBin"
        assert isinstance(volume, (int, float))

        if location.point.x ** 2 + location.point.y ** 2 > MAX_DRAW_RADIUS ** 2:
            raise ValueError(
                f'Dispensing outside safe area: ({location.point.x}, {location.point.y})'
                f' is more than {MAX_DRAW_RADIUS}mm from center.'
            )
        if not self.has_tip:
            raise RuntimeError("dispense() called without a tip")
        if self.current_volume < volume:
            raise ValueError(
                f"Dispensing {volume}µL but only {self.current_volume}µL in pipette."
            )
        if volume <= 0:
            raise ValueError(f"Dispense volume must be positive, got: {volume}µL")
        if location.point.z < 0:
            raise ValueError(f"dispense() with z={location.point.z} — cannot go below z=0")
        if location.point.z >= 10:
            print(f"⚠ Dispensing from z={location.point.z} — really that high?")

        self.smearIfJustDispensed(location)
        self.current_volume -= volume

        visual = resolve_visual_color(self.curr_color)
        self.droplets_x.append(location.point.x)
        self.droplets_y.append(location.point.y)
        self.droplets_size.append(volume * 100)  # scale factor: 1µL → 100 sq.pt
        self.droplets_color.append(visual)

        self.totalDispensed.setdefault(self.curr_color, 0)
        self.totalDispensed[self.curr_color] += volume
        self.location = location
        self.justDispensedAt = location

    def aspirate(self, volume: float, location: types.Location | WellMock) -> None:
        """Aspirate liquid from the given location.

        Args:
            volume: Volume in µL to aspirate.
            location: Source location (Well or types.Location).

        Raises:
            RuntimeError: If no tip is attached or cross-contamination detected.
            ValueError: If volume would exceed max pipette capacity.
        """
        assert isinstance(volume, (int, float))
        assert isinstance(location, (types.Location, WellMock))

        if not self.has_tip:
            raise RuntimeError("aspirate() called without a tip")
        if volume + self.current_volume > self.max_volume:
            raise ValueError(
                f"Aspirating {volume}µL + {self.current_volume}µL in pipette ="
                f" {volume + self.current_volume}µL > max {self.max_volume}µL"
            )
        if volume <= 0:
            raise ValueError(f"Aspirate volume must be positive, got: {volume}µL")
        if self.aspirated_loc is not None and self.aspirated_loc != location:
            raise RuntimeError(
                f"Cross-contamination between {self.aspirated_loc} and {location}"
            )

        self.aspirated_loc = location
        self.smearIfJustDispensed(location)
        self.current_volume += volume

        if isinstance(location, WellMock):
            if location.well_id.upper() not in (wid.upper() for wid in self.well_colors.keys()):
                raise ValueError(
                    f"aspirate() on well {location} which has no configured color."
                )
            color = location.color()
            newloc = location
        else:
            print("⚠ aspirate() with Location instead of Well — are you sure?")
            if location.point.z < 0:
                raise ValueError(f"aspirate() with z={location.point.z} — cannot go below z=0")
            color = 'white'
            newloc = location  # already a types.Location, use as-is

        self.curr_color = color
        self.totalAspirated.setdefault(color, 0)
        self.totalAspirated[color] += volume
        self.location = newloc

    def pick_up_tip(self) -> None:
        """Pick up a tip from the tip rack.

        Raises:
            RuntimeError: If a tip is already attached.
        """
        loc = types.Location(
            types.Point(x=-MAX_DRAW_RADIUS, y=MAX_DRAW_RADIUS, z=0), 'Pickup Tip'
        )
        self.smearIfJustDispensed(loc)
        if self.has_tip:
            raise RuntimeError("pick_up_tip() called while already holding a tip")
        self.has_tip = True
        assert self.aspirated_loc is None
        self.tip_count += 1
        self.current_volume = 0
        self.location = loc

    def drop_tip(self) -> None:
        """Drop the current tip.

        Raises:
            RuntimeError: If no tip is attached.
        """
        loc = types.Location(
            types.Point(x=MAX_DRAW_RADIUS, y=MAX_DRAW_RADIUS, z=0), 'Drop Tip'
        )
        self.smearIfJustDispensed(loc)
        if not self.has_tip:
            raise RuntimeError("drop_tip() called without a tip")
        self.has_tip = False
        self.aspirated_loc = None
        self.current_volume = 0
        self.location = loc

    def move_to(self, location: types.Location) -> None:
        """Move pipette to a location.

        Raises:
            ValueError: If z < 0.
        """
        if location.point.z < 0:
            raise ValueError(f"move_to() with z={location.point.z} — cannot go below z=0")
        self.smearIfJustDispensed(location)
        self.location = location

    def blow_out(self, location: object = None) -> None:
        """Blow out remaining liquid (visual no-op)."""
        self.current_volume = 0
        _mock_print("Blow out", self.verbose)

    def touch_tip(self, **kwargs: object) -> None:
        """Touch the tip against well walls (visual no-op)."""
        _mock_print("Touch tip", self.verbose)

    def mix(self, repetitions: int = 1, volume: Optional[float] = None,
            location: object = None) -> None:
        """Mix by aspirating and dispensing (visual no-op)."""
        _mock_print(f"Mix {repetitions}x", self.verbose)

    # ──── Visualization ────

    def visualize(self, **kwargs: object) -> tuple:
        """Generate the Petri dish visualization with all recorded droplets.

        Delegates to visualization.visualize_petri() with all accumulated data.

        Keyword Args:
            background: 'black' (dark agar), 'agar' (beige), or 'paper' (outline).
            title: Plot title string.
            save_path: File path to save the image.
            show: Whether to display the plot.
            dpi: Image resolution for saving.

        Returns:
            Tuple of (Figure, Axes).
        """
        return visualize_petri(
            droplets_x=self.droplets_x,
            droplets_y=self.droplets_y,
            droplets_size=self.droplets_size,
            droplets_color=self.droplets_color,
            smears=self.smears,
            total_aspirated=self.totalAspirated,
            total_dispensed=self.totalDispensed,
            tip_count=self.tip_count,
            **kwargs,
        )


# ═══════════════════════════════════════════════════════════════════════
# OpentronsMock — Entry point: simulates ProtocolContext
# ═══════════════════════════════════════════════════════════════════════

class OpentronsMock:
    """Simulates the Opentrons ProtocolContext.

    Drop-in replacement for ``protocol`` in ``run(protocol)`` functions
    generated by the Opentrons Art Designer or custom HTGAA protocols.

    Usage::

        from opentrons_bioart_sim import OpentronsMock

        mock = OpentronsMock(well_colors)
        run(mock)
        mock.visualize(background='black', save_path='output.png')
    """

    def __init__(self, well_colors: Optional[dict[str, str]] = None,
                 verbose: bool = False) -> None:
        """Initialize the mock protocol context.

        Args:
            well_colors: Dict mapping well ID → protein/color name.
                         Example: {'A1': 'sfGFP', 'A2': 'mRFP1', ...}
            verbose: If True, print debug messages for each operation.
        """
        self.verbose = verbose
        self.well_colors = well_colors or {}
        self.pipette: Optional[PipetteSim] = None

    def home(self) -> None:
        """Simulate homing the robot."""
        _mock_print("Going home!", self.verbose)

    def load_labware(self, labware_official_name: str, deck_slot: int,
                     display_name: str = "") -> LabwareMock:
        """Load labware onto the deck."""
        _mock_print(f"Loaded {labware_official_name} in slot {deck_slot}", self.verbose)
        return LabwareMock(labware_official_name, deck_slot, display_name,
                          self.well_colors, self.verbose)

    def load_module(self, module_official_name: str, deck_slot: int = 0) -> ModuleMock:
        """Load a hardware module onto the deck."""
        _mock_print(f"Loaded module {module_official_name} in slot {deck_slot}", self.verbose)
        return ModuleMock(module_official_name, deck_slot, self.well_colors, self.verbose)

    def load_instrument(self, instrument_official_name: str, mount_LR: str,
                        tip_rack_list: list[LabwareMock]) -> PipetteSim:
        """Load a pipette instrument."""
        self.pipette = PipetteSim(
            instrument_official_name, mount_LR, tip_rack_list, self.well_colors,
            self.verbose,
        )
        return self.pipette

    def pause(self, msg: str = "") -> None:
        """Simulate a robot pause."""
        _mock_print(f"Robot pause: {msg}", self.verbose)

    def comment(self, msg: str = "") -> None:
        """Add a protocol comment."""
        _mock_print(f"Comment: {msg}", self.verbose)

    def delay(self, seconds: float = 0, minutes: float = 0, msg: str = "") -> None:
        """Simulate a delay."""
        _mock_print(f"Delay: {minutes}m {seconds}s — {msg}", self.verbose)

    def visualize(self, **kwargs: object) -> Optional[tuple]:
        """Generate the Petri dish visualization.

        Delegates to the loaded pipette's visualize() method.

        Returns:
            Tuple of (Figure, Axes) or None if no pipette was loaded.
        """
        if self.pipette:
            return self.pipette.visualize(**kwargs)
        else:
            print("No pipette loaded — nothing to visualize.")
            return None


# ═══════════════════════════════════════════════════════════════════════
# Convenience function
# ═══════════════════════════════════════════════════════════════════════

def simulate_protocol(
    protocol_file_path: str,
    well_colors: Optional[dict[str, str]] = None,
    background: str = 'black',
    title: str = 'Opentrons Bio-Art Simulation',
    save_path: Optional[str] = None,
    show: bool = True,
    dpi: int = 150,
    verbose: bool = False,
) -> OpentronsMock:
    """Load and run an Opentrons protocol file in simulation mode.

    This is the primary one-liner API for running protocols::

        from opentrons_bioart_sim import simulate_protocol
        mock = simulate_protocol('my_design.py', background='agar')

    Args:
        protocol_file_path: Path to the .py protocol file (must have a ``run(protocol)`` function).
        well_colors: Dict mapping well ID → color/protein name. If None, uses
                     the protocol's own ``well_colors`` dict if present.
        background: Petri dish background: 'black', 'agar', or 'paper'.
        title: Title for the visualization plot.
        save_path: If provided, save the figure to this file path.
        show: Whether to display the plot window.
        dpi: Resolution for saved images.
        verbose: If True, print debug messages for each operation.

    Returns:
        The OpentronsMock instance used (for further inspection).

    Raises:
        FileNotFoundError: If the protocol file does not exist.
        AttributeError: If the protocol file has no ``run()`` function.
    """
    import importlib.util
    import os

    if not os.path.exists(protocol_file_path):
        raise FileNotFoundError(f"Protocol file not found: {protocol_file_path}")

    spec = importlib.util.spec_from_file_location("protocol_module", protocol_file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if not hasattr(mod, 'run'):
        raise AttributeError(
            f"Protocol file '{protocol_file_path}' has no run(protocol) function."
        )

    # Use the protocol's well_colors if not explicitly provided
    if well_colors is None and hasattr(mod, 'well_colors'):
        well_colors = mod.well_colors

    mock = OpentronsMock(well_colors, verbose=verbose)
    mod.run(mock)
    mock.visualize(
        background=background,
        title=title,
        save_path=save_path,
        show=show,
        dpi=dpi,
    )
    return mock
