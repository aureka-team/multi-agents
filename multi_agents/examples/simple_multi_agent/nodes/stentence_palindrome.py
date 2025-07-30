from langgraph.runtime import get_runtime

from multi_agents.graph import Node
from ..schema import StateSchema, ContextSchema


def run(state: StateSchema) -> dict:
    runtime = get_runtime(ContextSchema)

    if state.n_words is None:
        return {}

    if state.n_words >= dict(runtime.context)["min_sentence_words"]:
        return {
            "is_sentence_palindrome": True,
        }

    return {
        "is_sentence_palindrome": False,
    }


sentence_palindrome = Node(
    name="sentence_palindrome",
    run=run,
    is_finish_point=True,
)
