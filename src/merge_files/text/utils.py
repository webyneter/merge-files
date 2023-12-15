from merge_files.text.constants import TRIPLE_DOUBLE_QUOTE
from merge_files.text.constants import TRIPLE_SINGLE_QUOTE
from merge_files.text.models import UnbalancedTripleQuotesInText


def check_unbalanced_triple_quotes(text: str) -> UnbalancedTripleQuotesInText:
    """
    Check if the given string has unbalanced triple quotes.
    """
    has_unbalanced_triple_single_quote = text.count(TRIPLE_SINGLE_QUOTE) % 2 != 0
    has_unbalanced_triple_double_quote = text.count(TRIPLE_DOUBLE_QUOTE) % 2 != 0

    rightmost_unbalanced_triple_single_quote_index: int | None = None
    rightmost_unbalanced_triple_double_quote_index: int | None = None
    if has_unbalanced_triple_single_quote:
        rightmost_unbalanced_triple_single_quote_index = text.rfind(TRIPLE_SINGLE_QUOTE)
    if has_unbalanced_triple_double_quote:
        rightmost_unbalanced_triple_double_quote_index = text.rfind(TRIPLE_DOUBLE_QUOTE)

    if has_unbalanced_triple_single_quote and has_unbalanced_triple_double_quote:
        unbalanced_triple_single_quote_comes_first = (
            rightmost_unbalanced_triple_single_quote_index < rightmost_unbalanced_triple_double_quote_index
        )
        unbalanced_triple_double_quote_comes_first = not unbalanced_triple_single_quote_comes_first
    else:
        unbalanced_triple_single_quote_comes_first = has_unbalanced_triple_single_quote
        unbalanced_triple_double_quote_comes_first = has_unbalanced_triple_double_quote

    return UnbalancedTripleQuotesInText(
        text=text,
        has_unbalanced_triple_single_quote=has_unbalanced_triple_single_quote,
        has_unbalanced_triple_double_quote=has_unbalanced_triple_double_quote,
        unbalanced_triple_single_quote_comes_first=unbalanced_triple_single_quote_comes_first,
        unbalanced_triple_double_quote_comes_first=unbalanced_triple_double_quote_comes_first,
    )
