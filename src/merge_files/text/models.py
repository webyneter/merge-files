from pydantic import BaseModel


class UnbalancedTripleQuotesInText(BaseModel):
    """
    Contains information about unbalanced triple quotes in a string.

    Attributes:
        text: The string to check.
        has_unbalanced_triple_single_quote: Whether the string has unbalanced triple single quotes.
        has_unbalanced_triple_double_quote: Whether the string has unbalanced triple double quotes.
        unbalanced_triple_single_quote_comes_first: Whether the unbalanced triple single quote comes first.
        unbalanced_triple_double_quote_comes_first: Whether the unbalanced triple double quote comes first.
    """

    text: str
    has_unbalanced_triple_single_quote: bool
    has_unbalanced_triple_double_quote: bool
    unbalanced_triple_single_quote_comes_first: bool
    unbalanced_triple_double_quote_comes_first: bool
