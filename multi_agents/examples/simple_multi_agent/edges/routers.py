from collections.abc import Hashable

from langgraph.graph import END
from ..schema import StateSchema


def palindrome_num_words_router(state: StateSchema) -> list[Hashable]:
    if state.is_palindrome:
        return ["num_words"]

    return [END]
