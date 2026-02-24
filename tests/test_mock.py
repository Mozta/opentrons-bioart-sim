"""Tests for mock Opentrons API classes."""

import pytest
from opentrons import types

from opentrons_bioart_sim.mock import (
    LabwareMock,
    ModuleMock,
    OpentronsMock,
    PipetteSim,
    WellMock,
)


# ── Fixtures ──

SAMPLE_WELL_COLORS = {
    'A1': 'sfGFP',
    'A2': 'mRFP1',
    'A3': 'Azurite',
}


@pytest.fixture
def mock():
    return OpentronsMock(SAMPLE_WELL_COLORS)


@pytest.fixture
def loaded_mock(mock):
    """A mock with labware and pipette loaded, ready for operations."""
    tips = mock.load_labware('opentrons_96_tiprack_20ul', 9, '20uL Tips')
    pipette = mock.load_instrument('p20_single_gen2', 'right', [tips])
    plate = mock.load_labware('nest_96_wellplate_2ml_deep', 6)
    agar = mock.load_labware('htgaa_agar_plate', 5, 'Agar')
    return mock, pipette, plate, agar


# ── WellMock tests ──

class TestWellMock:
    def test_well_id_and_color(self):
        well = WellMock('A1', 'sfGFP', None)
        assert well.well_id == 'A1'
        assert well.color() == 'sfGFP'
        assert well.visual_color() == 'lime'

    def test_get_row_col(self):
        well = WellMock('B3', 'mRFP1', None)
        row, col = well.get_row_col()
        assert row == ord('B')
        assert col == 3

    def test_set_row_col(self):
        well = WellMock('A1', '', None)
        well.set_row_col(ord('C'), 5)
        assert well.well_id == 'C5'

    def test_top_returns_location(self):
        well = WellMock('A1', 'sfGFP', None)
        loc = well.top()
        assert isinstance(loc, types.Location)
        assert loc.point.z == 0

    def test_top_with_z(self):
        well = WellMock('A1', 'sfGFP', None)
        loc = well.top(z=5)
        assert loc.point.z == 5

    def test_bottom_returns_self(self):
        well = WellMock('A1', 'sfGFP', None)
        assert well.bottom() is well
        assert well.bottom(z=2) is well

    def test_center_returns_self(self):
        well = WellMock('A1', 'sfGFP', None)
        assert well.center() is well

    def test_default_color_is_purple(self):
        well = WellMock('A1', '', None)
        assert well.well_color == 'purple'

    def test_repr(self):
        well = WellMock('B7', 'mRFP1', None)
        assert repr(well) == 'B7'

    def test_equality(self):
        w1 = WellMock('A1', 'sfGFP', None)
        w2 = WellMock('A1', 'sfGFP', None)
        assert w1 == w2


# ── LabwareMock tests ──

class TestLabwareMock:
    def test_well_access(self):
        lw = LabwareMock('test_plate', 1, 'Test', SAMPLE_WELL_COLORS)
        well = lw.well('A1')
        assert isinstance(well, WellMock)
        assert well.well_id == 'A1'

    def test_bracket_access(self):
        lw = LabwareMock('test_plate', 1, 'Test', SAMPLE_WELL_COLORS)
        well = lw['A2']
        assert well.well_id == 'A2'
        assert well.color() == 'mRFP1'

    def test_wells_list(self):
        lw = LabwareMock('test_plate', 1, 'Test', SAMPLE_WELL_COLORS)
        wells = lw.wells()
        assert len(wells) == 3
        assert all(isinstance(w, WellMock) for w in wells)

    def test_set_offset_noop(self):
        lw = LabwareMock('test_plate', 1, 'Test', SAMPLE_WELL_COLORS)
        lw.set_offset(x=1, y=2, z=3)  # Should not raise

    def test_repr(self):
        lw = LabwareMock('test_plate', 5, 'My Plate', SAMPLE_WELL_COLORS)
        assert 'Deck Slot 5' in repr(lw)
        assert 'My Plate' in repr(lw)


# ── ModuleMock tests ──

class TestModuleMock:
    def test_load_labware(self):
        mod = ModuleMock('temperatureModuleV2', 3, SAMPLE_WELL_COLORS)
        lw = mod.load_labware('nest_96_wellplate_2ml_deep', 'Deep Plate')
        assert isinstance(lw, LabwareMock)

    def test_set_temperature(self):
        mod = ModuleMock('temperatureModuleV2', 3, {})
        mod.set_temperature(37)  # Should not raise

    def test_thermocycler_methods(self):
        mod = ModuleMock('thermocyclerModuleV2', 7, {})
        mod.open_lid()
        mod.close_lid()
        mod.set_lid_temperature(105)
        mod.deactivate_lid()
        mod.set_block_temperature(95, hold_time_seconds=30)
        mod.execute_profile(
            steps=[{'temperature': 95, 'hold_time_seconds': 10}],
            repetitions=30,
            block_max_volume=25,
        )


# ── PipetteSim tests ──

class TestPipetteSim:
    def test_pick_up_and_drop_tip(self, loaded_mock):
        _, pipette, _, _ = loaded_mock
        pipette.pick_up_tip()
        assert pipette.has_tip
        assert pipette.tip_count == 1
        pipette.drop_tip()
        assert not pipette.has_tip

    def test_pick_up_tip_twice_raises(self, loaded_mock):
        _, pipette, _, _ = loaded_mock
        pipette.pick_up_tip()
        with pytest.raises(RuntimeError, match="already holding"):
            pipette.pick_up_tip()
        pipette.drop_tip()

    def test_drop_tip_without_tip_raises(self, loaded_mock):
        _, pipette, _, _ = loaded_mock
        with pytest.raises(RuntimeError, match="without a tip"):
            pipette.drop_tip()

    def test_aspirate_dispense_cycle(self, loaded_mock):
        _, pipette, plate, agar = loaded_mock
        pipette.pick_up_tip()
        pipette.aspirate(5, plate['A1'])
        assert pipette.current_volume == 5

        loc = agar['A1'].top().move(types.Point(0, 0, 0))
        pipette.dispense(3, loc)
        assert pipette.current_volume == 2

        pipette.drop_tip()

    def test_aspirate_without_tip_raises(self, loaded_mock):
        _, pipette, plate, _ = loaded_mock
        with pytest.raises(RuntimeError, match="without a tip"):
            pipette.aspirate(5, plate['A1'])

    def test_dispense_without_tip_raises(self, loaded_mock):
        _, pipette, _, agar = loaded_mock
        loc = agar['A1'].top().move(types.Point(0, 0, 0))
        with pytest.raises(RuntimeError, match="without a tip"):
            pipette.dispense(5, loc)

    def test_over_aspirate_raises(self, loaded_mock):
        _, pipette, plate, _ = loaded_mock
        pipette.pick_up_tip()
        with pytest.raises(ValueError, match="max"):
            pipette.aspirate(25, plate['A1'])  # max is 20
        pipette.drop_tip()

    def test_over_dispense_raises(self, loaded_mock):
        _, pipette, plate, agar = loaded_mock
        pipette.pick_up_tip()
        pipette.aspirate(5, plate['A1'])
        loc = agar['A1'].top().move(types.Point(0, 0, 0))
        with pytest.raises(ValueError, match="only"):
            pipette.dispense(10, loc)
        pipette.drop_tip()

    def test_droplet_tracking(self, loaded_mock):
        _, pipette, plate, agar = loaded_mock
        pipette.pick_up_tip()
        pipette.aspirate(5, plate['A1'])

        loc = agar['A1'].top().move(types.Point(1, 2, 0))
        pipette.dispense(2, loc)

        assert len(pipette.droplets_x) == 1
        assert pipette.droplets_x[0] == 1
        assert pipette.droplets_y[0] == 2
        assert pipette.droplets_size[0] == 200  # 2µL * 100

        pipette.drop_tip()

    def test_noop_methods(self, loaded_mock):
        _, pipette, _, _ = loaded_mock
        pipette.blow_out()
        pipette.touch_tip()
        pipette.mix(repetitions=3)


# ── OpentronsMock tests ──

class TestOpentronsMock:
    def test_load_labware(self, mock):
        lw = mock.load_labware('opentrons_96_tiprack_20ul', 9, 'Tips')
        assert isinstance(lw, LabwareMock)

    def test_load_module(self, mock):
        mod = mock.load_module('temperatureModuleV2', 3)
        assert isinstance(mod, ModuleMock)

    def test_load_instrument(self, mock):
        tips = mock.load_labware('opentrons_96_tiprack_20ul', 9)
        pipette = mock.load_instrument('p20_single_gen2', 'right', [tips])
        assert isinstance(pipette, PipetteSim)
        assert mock.pipette is pipette

    def test_noop_methods(self, mock):
        mock.home()
        mock.pause("testing")
        mock.comment("hello")
        mock.delay(seconds=5, minutes=1, msg="waiting")

    def test_visualize_without_pipette(self, mock):
        result = mock.visualize(show=False)
        assert result is None

    def test_unsupported_pipette_raises(self, mock):
        tips = mock.load_labware('opentrons_96_tiprack_20ul', 9)
        with pytest.raises(ValueError, match="Unsupported pipette"):
            mock.load_instrument('p300_single_gen2', 'right', [tips])

    def test_unsupported_mount_raises(self, mock):
        tips = mock.load_labware('opentrons_96_tiprack_20ul', 9)
        with pytest.raises(ValueError, match="Unsupported mount"):
            mock.load_instrument('p20_single_gen2', 'left', [tips])


# ── Additional edge-case tests ──

class TestPipetteSimEdgeCases:
    def test_move_to_negative_z_raises(self, loaded_mock):
        _, pipette, _, _ = loaded_mock
        with pytest.raises(ValueError, match="cannot go below z=0"):
            pipette.move_to(types.Location(types.Point(0, 0, -1), None))

    def test_negative_aspirate_volume_raises(self, loaded_mock):
        _, pipette, plate, _ = loaded_mock
        pipette.pick_up_tip()
        with pytest.raises(ValueError, match="positive"):
            pipette.aspirate(-1, plate['A1'])
        pipette.drop_tip()

    def test_negative_dispense_volume_raises(self, loaded_mock):
        _, pipette, plate, agar = loaded_mock
        pipette.pick_up_tip()
        pipette.aspirate(5, plate['A1'])
        loc = agar['A1'].top().move(types.Point(0, 0, 0))
        with pytest.raises(ValueError, match="positive"):
            pipette.dispense(-1, loc)
        pipette.drop_tip()

    def test_smear_is_recorded(self, loaded_mock):
        """Dispensing then moving should record a smear."""
        _, pipette, plate, agar = loaded_mock
        pipette.pick_up_tip()
        pipette.aspirate(10, plate['A1'])
        loc1 = agar['A1'].top().move(types.Point(0, 0, 0))
        pipette.dispense(2, loc1)
        # Move to a different location right after dispensing (triggers smear)
        loc2 = agar['A1'].top().move(types.Point(5, 5, 0))
        pipette.dispense(2, loc2)
        assert len(pipette.smears) >= 1
        pipette.drop_tip()

    def test_cross_contamination_raises(self, loaded_mock):
        """Aspirating from two different wells without dropping tip raises."""
        _, pipette, plate, _ = loaded_mock
        pipette.pick_up_tip()
        pipette.aspirate(5, plate['A1'])
        with pytest.raises(RuntimeError, match="Cross-contamination"):
            pipette.aspirate(5, plate['A2'])
        pipette.drop_tip()


class TestModuleMockEdgeCases:
    def test_float_temperature(self):
        """Module should accept float temperatures."""
        mod = ModuleMock('temperatureModuleV2', 3, {})
        mod.set_temperature(37.5)  # Should not raise

    def test_temperature_out_of_range_raises(self):
        mod = ModuleMock('temperatureModuleV2', 3, {})
        with pytest.raises(AssertionError):
            mod.set_temperature(3)  # Below 4

    def test_float_lid_temperature(self):
        mod = ModuleMock('thermocyclerModuleV2', 7, {})
        mod.set_lid_temperature(105.5)  # Should not raise


class TestVerboseMode:
    def test_verbose_propagates(self, capsys):
        """Verbose=True should produce debug output."""
        mock = OpentronsMock(SAMPLE_WELL_COLORS, verbose=True)
        mock.home()
        captured = capsys.readouterr()
        assert "Going home" in captured.out

    def test_non_verbose_is_silent(self, capsys):
        """Verbose=False should not produce debug output."""
        mock = OpentronsMock(SAMPLE_WELL_COLORS, verbose=False)
        mock.home()
        captured = capsys.readouterr()
        assert "Going home" not in captured.out
