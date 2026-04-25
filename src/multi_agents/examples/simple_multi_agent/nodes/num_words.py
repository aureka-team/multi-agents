from typing import Any

from multi_agents.graph import Node
from ..schema import State


def run(state: State) -> dict[str, Any]:
    return {
        "n_words": len(state.message.split()),
    }


num_words = Node(
    name="num_words",
    run=run,
)
