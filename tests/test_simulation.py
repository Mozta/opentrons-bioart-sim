"""Tests for end-to-end protocol simulation."""

import os
import tempfile

import pytest

from opentrons_bioart_sim import simulate_protocol


EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'examples')


class TestSimulateProtocol:
    def test_octocat_runs_successfully(self):
        """Run the octocat example end-to-end without display."""
        protocol_path = os.path.join(EXAMPLES_DIR, 'octocat.py')
        if not os.path.exists(protocol_path):
            pytest.skip("octocat.py example not found")

        mock = simulate_protocol(protocol_path, show=False)
        assert mock.pipette is not None
        assert mock.pipette.tip_count > 0
        assert len(mock.pipette.droplets_x) > 0

    def test_simulate_with_save(self):
        """Verify that --save creates an image file."""
        protocol_path = os.path.join(EXAMPLES_DIR, 'octocat.py')
        if not os.path.exists(protocol_path):
            pytest.skip("octocat.py example not found")

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            save_path = f.name

        try:
            simulate_protocol(protocol_path, show=False, save_path=save_path)
            assert os.path.exists(save_path)
            assert os.path.getsize(save_path) > 0
        finally:
            if os.path.exists(save_path):
                os.unlink(save_path)

    def test_file_not_found_raises(self):
        with pytest.raises(FileNotFoundError):
            simulate_protocol('nonexistent_protocol.py', show=False)

    def test_different_backgrounds(self):
        """Verify all three background options work without error."""
        protocol_path = os.path.join(EXAMPLES_DIR, 'octocat.py')
        if not os.path.exists(protocol_path):
            pytest.skip("octocat.py example not found")

        for bg in ['black', 'agar', 'paper']:
            mock = simulate_protocol(protocol_path, background=bg, show=False)
            assert mock.pipette is not None
