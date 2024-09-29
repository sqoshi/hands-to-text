import pytest
from tabulate import tabulate

from hands_to_text.text import TextProcessor
from hands_to_text.text.strategy import (
    AutoCorrectionStrategy,
    FilterContiniousSymbolsStrategy,
    LeverageLanguageModelStrategy,
    RemoveRepetitionsStrategy,
)

GLOBAL_TEST_CASES = [
    ("HHHHHEEEEEELLLLLOOOOOO", "HELLO"),
    ("AAAABBBCCCDDDDEEEE", "ABCDE"),
    ("TTHHHEEEELLLLLOOOO", "THELO"),
    ("THHISSSSSS IIIISSSS A TTEEEESST", "THIS IS A TEST"),
    ("AAAAAAAABBBBCCCCDDDD", "ABCD"),
    (
        "TTThhee ccoommmaandd wiiiilllll ttakkeee iimmmaagesss foor dddiffereentt cllasseess (succh as thhe aaallphabettt in ssignn llaanguagge) aandd sttoorree thhem in ttthhe sppecfiiieed ddiiirreecttoorrryy. EEaacch cllassss wiiill hhhaave bby iimmmaagess colllected ussiiing llannnddmarkk detectiiionnn. TThhe colllecttionn wiiilll ccconttinuuue untiill all iimmmagesss aarree gathheereed ffoor eeach cllassss",
        "The command will take images for different classes (such as the alphabet in sign language) and store them in the specified directory. Each class will have images collected using landmark detection. The collection will continue until all images are gathered for each class",
    ),
    (
        "TTThxeecoFmmmawndddwIillllttakzeeiKmmaagvesssfDoorrddiffvrenttclRaassess(suucchasvthBheeaaallphabetktinssiggnnqllahanguaggee)aanddstbtoorrethjemRinmthhesppnecfiGieedddiiirOrecttoryy.EEEaacxhchhhclflassswiiiillhhhhaavvTebbyiimmaagessfcolFllecteddvuujsingllahnnndmarrkkdetectHionnn.TTphhhecolllectzioonhwiillklcconntinnueuntilallQimmaagesxsaarregaytherredfooreeeachhclxlassss",
        "The command will take images for different classes (such as the alphabet in sign language) and store them in the specified directory. Each class will have images collected using landmark detection. The collection will continue until all images are gathered for each class",
    ),
]


@pytest.fixture(
    params=[
        [RemoveRepetitionsStrategy],
        [FilterContiniousSymbolsStrategy],
        [AutoCorrectionStrategy],
        # [LeverageLanguageModelStrategy],
        # [RemoveRepetitionsStrategy, FilterContiniousSymbolsStrategy],
        # [RemoveRepetitionsStrategy, LeverageLanguageModelStrategy],
        # [FilterContiniousSymbolsStrategy, LeverageLanguageModelStrategy],
        # [
        #     RemoveRepetitionsStrategy,
        #     FilterContiniousSymbolsStrategy,
        #     LeverageLanguageModelStrategy,
        # ],
    ]
)
def text_processor(request):
    strategies = [strategy() for strategy in request.param]
    return TextProcessor(strategies)


results = []


def accuracy_check(output: str, expected: str) -> float:
    total_chars = len(expected)
    matched_chars = sum(e == o for e, o in zip(expected, output))
    return matched_chars / total_chars if total_chars > 0 else 0.0


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
    assert accuracy > 0.5


# @pytest.hookimpl(tryfirst=True)
# def pytest_runtest_makereport(item, call):
#     if call.when == "call" and call.excinfo is not None:
#         item.user_properties.append(("test_status", "failed"))
#     else:
#         item.user_properties.append(("test_status", "passed"))


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    if call.when == "call":
        outcome = call.excinfo
        try:
            test_outcome = "failed" if outcome else "passed"
            table = [
                [r["input"], r["output"], r["expected"], f"{r['accuracy']:.2f}"]
                for r in results
            ]

            print("\nTest Summary:")
            t = tabulate(
                table,
                headers=["Input", "Output", "Expected", "Accuracy"],
                tablefmt="grid",
            )
            print(t)

            with open("tests_summary.txt", "w") as f:
                f.write(t)
        except Exception as e:
            print("ERROR:", e)


# @pytest.hookimpl(tryfirst=True)
# def pytest_terminal_summary(terminalreporter, exitstatus, config):
#     table = [
#         [r["input"], r["output"], r["expected"], f"{r['accuracy']:.2f}"]
#         for r in results
#     ]

#     print("\nTest Summary:")
#     t = tabulate(
#         table, headers=["Input", "Output", "Expected", "Accuracy"], tablefmt="grid"
#     )
#     print(t)

#     with open("tests_summary.txt", "w") as f:
#         f.write(t)
