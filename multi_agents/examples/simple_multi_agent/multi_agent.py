from multi_agents.graph import MultiAgentGraph

from .schema import StateSchema, ContextSchema
from .nodes import palindrome, num_words, sentence_palindrome
from .edges import palindrome_num_words, num_words_sentence_palindrome


def get_multi_agent() -> MultiAgentGraph:
    nodes = [
        palindrome,
        num_words,
        sentence_palindrome,
    ]

    edges = [
        palindrome_num_words,
        num_words_sentence_palindrome,
    ]

    multi_agent = MultiAgentGraph(
        state_schema=StateSchema,
        context_schema=ContextSchema,
        nodes=nodes,
        edges=edges,
    )

    multi_agent.compile()
    return multi_agent
