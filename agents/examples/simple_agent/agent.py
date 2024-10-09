from agents.graph import AgentGraph

from .schema import StateSchema, ConfigSchema  # noqa
from .nodes.palindrome import palindrome  # noqa
from .nodes.num_words import num_words  # Noqa
from .nodes.stentence_palindrome import sentence_palindrome  # noqa

from .edges import palindrome_num_words, num_words_sentence_palindrome  # noqa


def get_agent() -> AgentGraph:
    nodes = [
        palindrome,
        num_words,
        sentence_palindrome,
    ]

    edges = [
        palindrome_num_words,
        num_words_sentence_palindrome,
    ]

    agent = AgentGraph(
        state_schema=StateSchema,
        config_schema=ConfigSchema,
        nodes=nodes,
        edges=edges,
    )

    agent.compile()
    return agent
