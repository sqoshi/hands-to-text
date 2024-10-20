# conftest.py

import pytest
from tabulate import tabulate

_text_results = []
_vid_results = []


@pytest.fixture(scope="session")
def text_results():
    """Fixture to store the test results."""
    return _text_results


@pytest.fixture(scope="session")
def vid_results():
    """Fixture to store the test results."""
    return _vid_results


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Generate a test summary after all tests have run."""
    text_table = [
        [
            r["processing_time"],
            r["strategies"],
            f"{r['accuracy']:.2f}",
            r["output"],
            r["input"],
            r["expected"],
        ]
        for r in _text_results
    ]

    tt = tabulate(
        text_table,
        headers=[
            "Processing Time",
            "Text Correction Stategies",
            "Accuracy",
            "Output",
            "Input",
            "Expected",
        ],
        tablefmt="github",
    )

    vid_table = [
        [
            r["processing_time"],
            r["video_path"],
            r["model"],
            r["strategies"],
            r["recognized_text"],
            r["output"],
            r["expected"],
        ]
        for r in _vid_results
    ]

    tv = tabulate(
        vid_table,
        headers=[
            "Processing Time",
            "Video Path",
            "Classification Model",
            "Text Correction Stategies",
            "Recognized Text",
            "Final Corrected Text",
            "Expected",
        ],
        tablefmt="github",
    )

    with open("experiments.md", "w") as f:
        f.write(f"# Experiments\n\n\n## Text\n\n{tt}\n\n\n## Video\n\n{tv}\n\n\n")
