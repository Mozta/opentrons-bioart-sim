"""Tests for the CLI entry point."""

import os
import tempfile

import pytest

from opentrons_bioart_sim.cli import main


EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'examples')


class TestCLI:
    def test_help_flag(self, capsys):
        """--help should print usage and exit 0."""
        with pytest.raises(SystemExit) as exc:
            main(['--help'])
        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert 'opentrons-bioart-sim' in captured.out

    def test_version_flag(self, capsys):
        """--version should print version and exit 0."""
        with pytest.raises(SystemExit) as exc:
            main(['--version'])
        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert '1.0.0' in captured.out

    def test_missing_protocol_arg(self):
        """No args should exit with error code 2."""
        with pytest.raises(SystemExit) as exc:
            main([])
        assert exc.value.code == 2

    def test_nonexistent_file_exits_1(self):
        """Non-existent file should exit with code 1."""
        with pytest.raises(SystemExit) as exc:
            main(['nonexistent_protocol.py'])
        assert exc.value.code == 1

    def test_run_example_no_show(self):
        """Run an example protocol via CLI with --no-show."""
        protocol_path = os.path.join(EXAMPLES_DIR, 'octocat.py')
        if not os.path.exists(protocol_path):
            pytest.skip("octocat.py example not found")

        # Should complete without raising
        main([protocol_path, '--no-show'])

    def test_save_flag_creates_file(self):
        """--save should create an output image file."""
        protocol_path = os.path.join(EXAMPLES_DIR, 'octocat.py')
        if not os.path.exists(protocol_path):
            pytest.skip("octocat.py example not found")

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            save_path = f.name

        try:
            main([protocol_path, '--no-show', '--save', save_path])
            assert os.path.exists(save_path)
            assert os.path.getsize(save_path) > 0
        finally:
            if os.path.exists(save_path):
                os.unlink(save_path)

    def test_background_agar(self):
        """--background agar should work."""
        protocol_path = os.path.join(EXAMPLES_DIR, 'octocat.py')
        if not os.path.exists(protocol_path):
            pytest.skip("octocat.py example not found")

        main([protocol_path, '--no-show', '--background', 'agar'])

    def test_verbose_flag(self):
        """--verbose should run without error."""
        protocol_path = os.path.join(EXAMPLES_DIR, 'octocat.py')
        if not os.path.exists(protocol_path):
            pytest.skip("octocat.py example not found")

        main([protocol_path, '--no-show', '--verbose'])
