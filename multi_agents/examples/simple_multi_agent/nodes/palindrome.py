from multi_agents.graph import Node
from ..schema import StateSchema, ConfigSchema


def run(state: StateSchema, config: ConfigSchema) -> StateSchema:
    message = state.message
    if "".join(reversed(message)) == message:
        return {"is_palindrome": True}

    return {"is_palindrome": False}


palindrome = Node(
    name="palindrome",
    run=run,
    is_entry_point=True,
)
