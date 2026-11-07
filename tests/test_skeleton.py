import subprocess
import sys

import pytest

import septum
from septum.cli import PLANNED_COMMANDS, main
from septum.exitcodes import Exit


def test_version_is_set():
    assert septum.__version__


def test_exit_codes_match_spec():
    assert (Exit.ALLOW, Exit.ERROR, Exit.DENY, Exit.ASK_PENDING) == (0, 1, 2, 3)


@pytest.mark.parametrize("command", sorted(PLANNED_COMMANDS))
def test_unbuilt_commands_fail_closed(command, capsys):
    assert main([command]) == Exit.DENY
    assert "not implemented" in capsys.readouterr().err


def test_bare_septum_denies_until_tui_exists():
    assert main([]) == Exit.DENY


def test_module_entry_point_runs():
    out = subprocess.run(
        [sys.executable, "-m", "septum", "--version"], capture_output=True, text=True
    )
    assert out.returncode == 0
    assert out.stdout.startswith("septum ")
