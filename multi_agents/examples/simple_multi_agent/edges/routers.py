from langgraph.graph import END
from ..schema import StateSchema, ConfigSchema


def palindrome_num_words_router(
    state: StateSchema,
    config: ConfigSchema,
) -> list[str]:
    if state.is_palindrome:
        return ["num_words"]

    return [END]
