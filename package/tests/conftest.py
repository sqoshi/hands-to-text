# conftest.py

import pytest
from tabulate import tabulate

_results = []


@pytest.fixture(scope="session")
def results():
    """Fixture to store the test results."""
    return _results


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Generate a test summary after all tests have run."""
    table = [
        [
            r["strategies"],
            f"{r['accuracy']:.2f}",
            r["input"],
            r["output"],
            r["expected"],
        ]
        for r in _results
    ]

    t = tabulate(
        table,
        headers=["Stategies", "Accuracy", "Input", "Output", "Expected"],
        tablefmt="github",
    )
    # print("\nTest Summary:")
    # print(t)

    with open("tests_summary.md", "w") as f:
        f.write(f"# Experiments summary\n\n{t}\n")
