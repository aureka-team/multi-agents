from multi_agents.graph import Node
from ..schema import StateSchema, ConfigSchema


def run(state: StateSchema, config: ConfigSchema) -> StateSchema:
    return {"n_words": len(state.message.split())}


num_words = Node(
    name="num_words",
    run=run,
)
