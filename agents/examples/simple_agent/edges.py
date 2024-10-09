from langgraph.graph import END

from agents.graph import SimpleEdge, ConditionalEdge
from agents.examples.simple_agent.schema import StateSchema, ConfigSchema


def palindrome_num_words_router(
    state: StateSchema,
    config: ConfigSchema,
) -> list[str]:
    if state.is_palindrome:
        return ["num_words"]

    return [END]


palindrome_num_words = ConditionalEdge(
    source="palindrome",
    intermediates=["num_words", END],
    router=palindrome_num_words_router,
)

num_words_sentence_palindrome = SimpleEdge(
    source="num_words",
    target="sentence_palindrome",
)
