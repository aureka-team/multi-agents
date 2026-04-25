from typing import Any
from langgraph.runtime import get_runtime

from multi_agents.graph import Node
from ..schema import State, Context


def run(state: State) -> dict[str, Any]:
    runtime = get_runtime(Context)

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
