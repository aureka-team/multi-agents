from collections.abc import Hashable

from langgraph.graph import END
from ..schema import State


def palindrome_num_words_router(state: State) -> list[Hashable]:
    if state.is_palindrome:
        return ["num_words"]

    return [END]
