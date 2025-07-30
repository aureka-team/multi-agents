from multi_agents.graph import Node
from ..schema import StateSchema


def run(state: StateSchema) -> dict:
    return {"n_words": len(state.message.split())}


num_words = Node(
    name="num_words",
    run=run,
)
