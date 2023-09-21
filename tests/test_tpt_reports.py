#!/usr/bin/env pytest -vs
"""Tests for tpt-reports."""

# Standard Python Libraries
import logging
import os
import sys
from unittest.mock import patch

# Third-Party Libraries
import pytest

# cisagov Libraries
import tpt_reports

log_levels = (
    "debug",
    "info",
    "warning",
    "error",
    "critical",
)

test_tpt_info = {
    "assessment_id": "test",
    "domain_tested": "cisa.gov",
    "election_name": "test",
    "output_directory": "./test_output",
    "payloads_meta": {
        "border_blocked": 1,
        "border_not_blocked": 1,
        "host_blocked": 1,
        "host_not_blocked": 1,
        "num_payloads": 4,
        "payloads_blocked": 2,
        "payloads_not_blocked": 2,
    },
}

test_payloads_list = [
    {
        "border_protection": "Blocked",
        "C2_Protocol": "test_protocol",
        "host_protection": "Not blocked",
        "Payload": "test_payload_1",
    },
    {
        "border_protection": "Not blocked",
        "C2_Protocol": "test_protocol",
        "host_protection": "Blocked",
        "Payload": "test_payload_2",
    },
]

# define sources of version strings
RELEASE_TAG = os.getenv("RELEASE_TAG")
PROJECT_VERSION = tpt_reports.__version__


def test_stdout_version(capsys):
    """Verify that version string sent to stdout agrees with the module version."""
    with pytest.raises(SystemExit):
        with patch.object(sys, "argv", ["bogus", "--version"]):
            tpt_reports.tpt_reports.main()
    captured = capsys.readouterr()
    assert (
        captured.out == f"{PROJECT_VERSION}\n"
    ), "standard output by '--version' should agree with module.__version__"


def test_running_as_module(capsys):
    """Verify that the __main__.py file loads correctly."""
    with pytest.raises(SystemExit):
        with patch.object(sys, "argv", ["bogus", "--version"]):
            # F401 is a "Module imported but unused" warning. This import
            # emulates how this project would be run as a module. The only thing
            # being done by __main__ is importing the main entrypoint of the
            # package and running it, so there is nothing to use from this
            # import. As a result, we can safely ignore this warning.
            # cisagov Libraries
            import tpt_reports.__main__  # noqa: F401
    captured = capsys.readouterr()
    assert (
        captured.out == f"{PROJECT_VERSION}\n"
    ), "standard output by '--version' should agree with module.__version__"


@pytest.mark.skipif(
    RELEASE_TAG in [None, ""], reason="this is not a release (RELEASE_TAG not set)"
)
def test_release_version():
    """Verify that release tag version agrees with the module version."""
    assert (
        RELEASE_TAG == f"v{PROJECT_VERSION}"
    ), "RELEASE_TAG does not match the project version"


@pytest.mark.parametrize("level", log_levels)
def test_log_levels(level):
    """Validate commandline log-level arguments."""
    with patch.object(
        sys,
        "argv",
        [
            "bogus",
            f"--log-level={level}",
            "test",
            "test",
            "cisa.gov",
            "test.json",
            "./test_output",
        ],
    ):
        with patch.object(logging.root, "handlers", []):
            assert (
                logging.root.hasHandlers() is False
            ), "root logger should not have handlers yet"
            return_code = None
            try:
                tpt_reports.tpt_reports.main()
            except SystemExit as sys_exit:
                return_code = sys_exit.code
            assert return_code is None, "main() should return success"
            assert (
                logging.root.hasHandlers() is True
            ), "root logger should now have a handler"
            assert (
                logging.getLevelName(logging.root.getEffectiveLevel()) == level.upper()
            ), f"root logger level should be set to {level.upper()}"
            assert return_code is None, "main() should return success"


def test_bad_log_level():
    """Validate bad log-level argument returns error."""
    with patch.object(
        sys,
        "argv",
        ["bogus", "--log-level=emergency", "test", "test", "test", "test", "test"],
    ):
        return_code = None
        try:
            tpt_reports.tpt_reports.main()
        except SystemExit as sys_exit:
            return_code = sys_exit.code
        assert return_code == 1, "main() should exit with error return code 1"


def test_domain_validation():
    """Validate invalid domain arguments."""
    with patch.object(
        sys,
        "argv",
        [
            "bogus",
            "--log-level=debug",
            "test",
            "test",
            "cisa",
            "test.json",
            "./test_output",
        ],
    ):
        return_code = None
        try:
            tpt_reports.tpt_reports.main()
        except SystemExit as sys_exit:
            return_code = sys_exit.code
            assert return_code == 2, "main() should return with error return code 2"


def test_generate_reports():
    """Validate report generation."""
    result = tpt_reports.tpt_reports.report_gen(test_tpt_info, test_payloads_list)
    assert isinstance(
        result, tpt_reports.report_generator.MyDocTemplate
    ), "generate_reports did not return an object of type MyDocTemplate"

    with pytest.raises(TypeError) as excinfo:
        result = tpt_reports.tpt_reports.report_gen(None, None)
    assert isinstance(
        excinfo.value, TypeError
    ), "report_gen() did not correctly handle a NoneType argument."
