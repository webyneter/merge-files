import pytest

from merge_files.text.utils import check_unbalanced_triple_quotes


@pytest.mark.parametrize(
    (
        "text",
        "expected_has_unbalanced_triple_single_quote",
        "expected_has_unbalanced_triple_double_quote",
        "expected_unbalanced_triple_single_quote_comes_first",
        "expected_unbalanced_triple_double_quote_comes_first",
    ),
    [
        ("", False, False, False, False),  # Empty string
        ("'''", True, False, True, False),  # Only opens triple single quotes
        ('"""', False, True, False, True),  # Only opens triple double quotes
        ("''''''", False, False, False, False),  # Opens and closes triple single quotes
        ('""""""', False, False, False, False),  # Opens and closes triple double quotes
        ("''' ''''''", True, False, True, False),  # Opens and closes triple single quotes, but leaves a single quote
        ("'''''' '''", True, False, True, False),  # Opens and closes triple single quotes, but leaves a single quote
        ("''' and some text '''", False, False, False, False),  # Closes the triple single quotes
        ('""" and some text """', False, False, False, False),  # Closes the triple double quotes
        ("''' and some text", True, False, True, False),  # Opens but does not close triple single quotes
        ('""" and some text', False, True, False, True),  # Opens but does not close triple double quotes
        ("''' and some text ''' plus '''", True, False, True, False),  # Opens another triple single quotes
        ('""" and some text """ plus """', False, True, False, True),  # Opens another triple double quotes
        ("No triple quotes here", False, False, False, False),  # No triple quotes
        (
            "''' and ''' mixed with \"\"\" quotes",
            False,
            True,
            False,
            True,
        ),  # Mixed quotes, only opens triple double quotes
        (
            "''' and ''' mixed with ''' quotes",
            True,
            False,
            True,
            False,
        ),  # Mixed quotes, only opens triple single quotes
        (
            "''' and some ''' text with \"\"\" unbalanced quotes",
            False,
            True,
            False,
            True,
        ),  # Mixed quotes, only opens triple double quotes
        (
            "Some text with \"\"\" unbalanced quotes and '''",
            True,
            True,
            False,
            True,
        ),  # Mixed quotes, opens both triple single and double quotes
    ],
)
def test_succeeds(
    text: str,
    expected_has_unbalanced_triple_single_quote: bool,
    expected_has_unbalanced_triple_double_quote: bool,
    expected_unbalanced_triple_single_quote_comes_first: bool,
    expected_unbalanced_triple_double_quote_comes_first: bool,
):
    """
    Test that the function returns the expected result for the given input.
    """
    result = check_unbalanced_triple_quotes(text)

    assert result.text == text
    assert result.has_unbalanced_triple_single_quote == expected_has_unbalanced_triple_single_quote
    assert result.has_unbalanced_triple_double_quote == expected_has_unbalanced_triple_double_quote
    assert result.unbalanced_triple_single_quote_comes_first == expected_unbalanced_triple_single_quote_comes_first
    assert result.unbalanced_triple_double_quote_comes_first == expected_unbalanced_triple_double_quote_comes_first
