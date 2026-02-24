"""Tests for color resolution and protein mapping."""

from opentrons_bioart_sim.colors import (
    PROTEIN_VISUAL_COLORS,
    resolve_visual_color,
)


class TestProteinColorMapping:
    """Tests for the PROTEIN_VISUAL_COLORS dictionary."""

    def test_known_proteins_all_have_string_values(self):
        for protein, color in PROTEIN_VISUAL_COLORS.items():
            assert isinstance(protein, str)
            assert isinstance(color, str)
            assert len(color) > 0

    def test_sfgfp_is_lime(self):
        assert PROTEIN_VISUAL_COLORS['sfgfp'] == 'lime'

    def test_mrfp1_is_red(self):
        assert PROTEIN_VISUAL_COLORS['mrfp1'] == 'red'

    def test_azurite_is_royalblue(self):
        assert PROTEIN_VISUAL_COLORS['azurite'] == 'royalblue'


class TestResolveVisualColor:
    """Tests for the resolve_visual_color function."""

    def test_known_protein(self):
        assert resolve_visual_color('sfGFP') == 'lime'

    def test_case_insensitive(self):
        assert resolve_visual_color('SFGFP') == 'lime'
        assert resolve_visual_color('SfGfP') == 'lime'
        assert resolve_visual_color('sfgfp') == 'lime'

    def test_with_whitespace(self):
        assert resolve_visual_color(' sfGFP ') == 'lime'

    def test_green_maps_to_lime(self):
        assert resolve_visual_color('green') == 'lime'
        assert resolve_visual_color('Green') == 'lime'

    def test_passthrough_unknown_color(self):
        assert resolve_visual_color('magenta') == 'magenta'
        assert resolve_visual_color('#ff0000') == '#ff0000'

    def test_all_protein_categories(self):
        """Verify at least one protein per color category resolves."""
        assert resolve_visual_color('mcherry') == 'firebrick'    # red
        assert resolve_visual_color('mko2') == 'orange'          # orange
        assert resolve_visual_color('venus') == 'yellow'         # yellow
        assert resolve_visual_color('mclover3') == 'green'       # green
        assert resolve_visual_color('tagbfp') == 'blue'          # blue
        assert resolve_visual_color('mplum') == 'purple'         # other
