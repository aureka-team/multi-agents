from langgraph.graph import END
from ..schema import StateSchema


def palindrome_num_words_router(state: StateSchema) -> list[str]:
    if state.is_palindrome:
        return ["num_words"]

    return [END]
