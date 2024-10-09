from agents.graph import Node
from agents.examples.simple_agent.schema import StateSchema, ConfigSchema


def run(state: StateSchema, config: ConfigSchema) -> StateSchema:
    if state.n_words >= config["configurable"]["min_sentence_words"]:
        return {"is_sentence_palindrome": True}

    return {"is_sentence_palindrome": False}


sentence_palindrome = Node(
    name="sentence_palindrome",
    run=run,
    is_finish_point=True,
)
