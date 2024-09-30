import pytest
from tabulate import tabulate

from hands_to_text.text import TextProcessor, get_startegies_perms
from hands_to_text.text.strategy import (
    AutoCorrectionStrategy,
    ChatG4FStrategy,
    FilterContiniousSymbolsStrategy,
    LevenshteinCorrectionStrategy,
    LeverageLanguageModelStrategy,
    MajorityVoteStrategy,
    PhoneticCorrectionStrategy,
    RemoveRepetitionsStrategy,
    WordSegmentationStrategy,
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
        # [
        #     RemoveRepetitionsStrategy,
        #     FilterContiniousSymbolsStrategy,
        #     MajorityVoteStrategy,
        # ],
        # [
        #     AutoCorrectionStrategy,
        #     PhoneticCorrectionStrategy,
        # ],
        # [
        #     LeverageLanguageModelStrategy,
        #     WordSegmentationStrategy,
        #     PhoneticCorrectionStrategy,
        #     AutoCorrectionStrategy,
        # ],
        # [
        #     RemoveRepetitionsStrategy,
        #     FilterContiniousSymbolsStrategy,
        #     LeverageLanguageModelStrategy,
        #     WordSegmentationStrategy,
        # ],
        [ChatG4FStrategy],
        [LeverageLanguageModelStrategy],
    ]
)
def text_processor(request):
    strategies = [strategy() for strategy in request.param]
    return TextProcessor(strategies)


def accuracy_check(output: str, expected: str) -> float:
    total_chars = len(expected)
    matched_chars = sum(e == o for e, o in zip(expected, output))
    return matched_chars / total_chars if total_chars > 0 else 0.0


@pytest.mark.parametrize("input_text, expected_output", GLOBAL_TEST_CASES)
def test_strategy_combinations(
    text_processor, results, input_text: str, expected_output: str
):
    result = text_processor.process(input_text)
    accuracy = accuracy_check(result, expected_output)
    results.append(
        {
            "strategies": f"`{', '.join([str(_) for _ in text_processor.strategies])}`",
            "accuracy": accuracy,
            "input": input_text,
            "output": result,
            "expected": expected_output,
        }
    )
    # print(
    #     f"Input: {input_text}\nOutput: {result}\nExpected: {expected_output}\nAccuracy: {accuracy:.2f}\n"
    # )
    # assert accuracy > 0.5
