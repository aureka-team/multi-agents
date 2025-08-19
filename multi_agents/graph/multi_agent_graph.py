from collections.abc import Hashable
from pydantic import BaseModel, StrictStr, StrictBool, ConfigDict
from typing import Type, Callable, Literal, TypeVar, Generic, Awaitable, Any

from common.logger import get_logger
from IPython.display import Image, display

from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import InMemorySaver


logger = get_logger(__name__)


StateT = TypeVar("StateT", bound=BaseModel)
ContextT = TypeVar("ContextT", bound=BaseModel)
RunType = Callable[[StateT], dict[str, Any] | Awaitable[dict[str, Any]]]


class Node(BaseModel, Generic[StateT]):
    name: StrictStr
    run: RunType
    is_entry_point: StrictBool = False
    is_finish_point: StrictBool = False


class ConditionalEdge(BaseModel, Generic[StateT]):
    source: StrictStr
    intermediates: list[StrictStr]
    router: Callable[[StateT], list[Hashable]]


class SimpleEdge(BaseModel):
    source: StrictStr | list[StrictStr]
    target: StrictStr


class MultiAgentGraph(BaseModel, Generic[StateT, ContextT]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    state_schema: Type[StateT]
    context_schema: Type[ContextT]
    nodes: list[Node[StateT]]
    edges: (
        list[SimpleEdge | ConditionalEdge]
        | list[SimpleEdge]
        | list[ConditionalEdge]
    )
    with_memory: StrictBool = True
    graph: CompiledStateGraph[StateT, ContextT, Any, Any] | None = None

    def compile(self) -> None:
        graph_builder = StateGraph(
            state_schema=self.state_schema,
            context_schema=self.context_schema,
        )

        # NOTE: Add nodes.
        for node in self.nodes:
            node_name = node.name
            graph_builder.add_node(node_name, node.run)

            if node.is_entry_point:
                graph_builder.set_entry_point(node_name)

            if node.is_finish_point:
                graph_builder.set_finish_point(node_name)

        # NOTE: Add edges.
        for edge in self.edges:
            if isinstance(edge, SimpleEdge):
                graph_builder.add_edge(edge.source, edge.target)
                continue

            if isinstance(edge, ConditionalEdge):
                graph_builder.add_conditional_edges(
                    edge.source,
                    edge.router,
                    edge.intermediates,
                )

        checkpointer = InMemorySaver() if self.with_memory else None
        self.graph = graph_builder.compile(checkpointer=checkpointer)

    def display_graph(
        self,
        draw_type: Literal[
            "ascii",
            "mermaid",
        ] = "ascii",
    ) -> None:
        if self.graph is None:
            logger.error("the graph was not created.")
            return

        match draw_type:
            case "ascii":
                ascii_graph = self.graph.get_graph().draw_ascii()
                print(ascii_graph)

            case "mermaid":
                graph_image = self.graph.get_graph().draw_mermaid_png()
                display(Image(graph_image))

    async def run(
        self,
        input_state: StateT,
        context: ContextT,
        thread_id: str,
    ) -> StateT | None:
        if self.graph is None:
            return

        state = await self.graph.ainvoke(
            input=input_state,
            context=context,
            config={
                "configurable": {
                    "thread_id": thread_id,
                },
            },
        )

        return self.state_schema(**state)
