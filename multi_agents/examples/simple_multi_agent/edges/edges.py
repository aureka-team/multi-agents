from langgraph.graph import END
from multi_agents.graph import SimpleEdge, ConditionalEdge

from .routers import palindrome_num_words_router


palindrome_num_words = ConditionalEdge(
    source="palindrome",
    intermediates=["num_words", END],
    router=palindrome_num_words_router,
)

num_words_sentence_palindrome = SimpleEdge(
    source="num_words",
    target="sentence_palindrome",
)
