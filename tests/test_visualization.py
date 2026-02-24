"""Tests for visualization module."""

import matplotlib
matplotlib.use('Agg')  # non-interactive backend for CI

from opentrons_bioart_sim.visualization import visualize_petri


class TestVisualizePetri:
    def _base_args(self):
        return dict(
            droplets_x=[0, 1, -1],
            droplets_y=[0, 1, -1],
            droplets_size=[100, 200, 150],
            droplets_color=['red', 'lime', 'blue'],
            smears=[],
            total_aspirated={'red': 5.0, 'lime': 3.0},
            total_dispensed={'red': 5.0, 'lime': 3.0},
            tip_count=2,
        )

    def test_returns_figure_and_axes(self):
        fig, ax = visualize_petri(**self._base_args(), show=False)
        assert fig is not None
        assert ax is not None

    def test_black_background(self):
        fig, ax = visualize_petri(**self._base_args(), background='black', show=False)
        patches = ax.patches
        assert len(patches) == 1  # the petri dish circle

    def test_agar_background(self):
        fig, ax = visualize_petri(**self._base_args(), background='agar', show=False)
        assert fig is not None

    def test_paper_background(self):
        fig, ax = visualize_petri(**self._base_args(), background='paper', show=False)
        assert fig is not None

    def test_unknown_background_defaults_to_black(self):
        fig, ax = visualize_petri(**self._base_args(), background='unknown', show=False)
        assert fig is not None

    def test_empty_droplets(self):
        fig, ax = visualize_petri(
            droplets_x=[], droplets_y=[], droplets_size=[], droplets_color=[],
            smears=[], total_aspirated={}, total_dispensed={}, tip_count=0,
            show=False,
        )
        assert fig is not None

    def test_with_smears(self):
        args = self._base_args()
        args['smears'] = [([0, 1], [0, 1], 'red')]
        fig, ax = visualize_petri(**args, show=False)
        assert len(ax.lines) >= 1

    def test_save_creates_file(self, tmp_path):
        save_path = str(tmp_path / 'test_output.png')
        fig, ax = visualize_petri(**self._base_args(), show=False, save_path=save_path)
        import os
        assert os.path.exists(save_path)
        assert os.path.getsize(save_path) > 0

    def test_waste_warning_printed(self, capsys):
        """If aspirated > dispensed, a WASTE warning should appear."""
        fig, ax = visualize_petri(
            droplets_x=[0], droplets_y=[0], droplets_size=[100], droplets_color=['red'],
            smears=[], total_aspirated={'red': 10.0}, total_dispensed={'red': 5.0},
            tip_count=1, show=False,
        )
        captured = capsys.readouterr()
        assert 'WASTE' in captured.out
