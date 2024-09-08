import pytest
from hands_to_text.text import TextProcessor
from hands_to_text.text.strategy import (
    FilterContiniousSymbolsStrategy,
    LeverageLanguageModelStrategy,
    RemoveRepetitionsStrategy,
)
from tabulate import tabulate

# Define global test cases with input and expected output
GLOBAL_TEST_CASES = [
    ("HHHHHEEEEEELLLLLOOOOOO", "HELLO"),
    ("AAAABBBCCCDDDDEEEE", "ABCDE"),
    ("TTHHHEEEELLLLLOOOO", "THELO"),
    ("THHISSSSSS IIIISSSS A TTEEEESST", "THIS IS A TEST"),
    ("AAAAAAAABBBBCCCCDDDD", "ABCD"),  # Complex test case
    (
        "TTThhee ccoommmaandd wiiiilllll ttakkeee iimmmaagesss foor dddiffereentt cllasseess (succh as thhe aaallphabettt in ssignn llaanguagge) aandd sttoorree thhem in ttthhe sppecfiiieed ddiiirreecttoorrryy. EEaacch cllassss wiiill hhhaave bby iimmmaagess colllected ussiiing llannnddmarkk detectiiionnn. TThhe colllecttionn wiiilll ccconttinuuue untiill all iimmmagesss aarree gathheereed ffoor eeach cllassss",
        "The command will take images for different classes (such as the alphabet in sign language) and store them in the specified directory. Each class will have images collected using landmark detection. The collection will continue until all images are gathered for each class",
    ),
]


# Define fixtures
@pytest.fixture
def remove_reps_strategy():
    return RemoveRepetitionsStrategy()


@pytest.fixture
def filter_symbols_strategy():
    return FilterContiniousSymbolsStrategy()


@pytest.fixture
def language_model_strategy():
    return LeverageLanguageModelStrategy()


# Define text processor fixture with various strategy combinations
@pytest.fixture(
    params=[
        [RemoveRepetitionsStrategy],
        [FilterContiniousSymbolsStrategy],
        [LeverageLanguageModelStrategy],
        [RemoveRepetitionsStrategy, FilterContiniousSymbolsStrategy],
        [RemoveRepetitionsStrategy, LeverageLanguageModelStrategy],
        [FilterContiniousSymbolsStrategy, LeverageLanguageModelStrategy],
        [
            RemoveRepetitionsStrategy,
            FilterContiniousSymbolsStrategy,
            LeverageLanguageModelStrategy,
        ],
    ]
)
def text_processor(request):
    strategies = [strategy() for strategy in request.param]
    return TextProcessor(strategies)


results = []


# Function to calculate accuracy between output and expected output
def accuracy_check(output: str, expected: str) -> float:
    total_chars = len(expected)
    matched_chars = sum(e == o for e, o in zip(expected, output))
    return matched_chars / total_chars if total_chars > 0 else 0.0


# Test for strategy combinations with given input and expected output
@pytest.mark.parametrize("input_text, expected_output", GLOBAL_TEST_CASES)
def test_strategy_combinations(text_processor, input_text: str, expected_output: str):
    result = text_processor.process(input_text)
    accuracy = accuracy_check(result, expected_output)
    results.append(
        {
            "input": input_text,
            "output": result,
            "expected": expected_output,
            "accuracy": accuracy,
        }
    )
    print(
        f"Input: {input_text}\nOutput: {result}\nExpected: {expected_output}\nAccuracy: {accuracy:.2f}\n"
    )


# Collect results and print table after all tests
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo is not None:
        item.user_properties.append(("test_status", "failed"))
    else:
        item.user_properties.append(("test_status", "passed"))


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if not config.option.tbstyle:
        return

    table = [
        [r["input"], r["output"], r["expected"], f"{r['accuracy']:.2f}"]
        for r in results
    ]
    print("\nTest Summary:")
    print(
        tabulate(
            table, headers=["Input", "Output", "Expected", "Accuracy"], tablefmt="grid"
        )
    )
