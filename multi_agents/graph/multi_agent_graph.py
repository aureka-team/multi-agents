from typing import Type, Callable, Literal
from pydantic import (
    BaseModel,
    StrictStr,
    StrictBool,
    Field,
)

from common.logger import get_logger
from IPython.display import Image, display

from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver


logger = get_logger(__name__)


StateSchema = BaseModel
ConfigSchema = BaseModel


class Node(BaseModel):
    name: StrictStr
    run: Callable[[StateSchema, ConfigSchema], StateSchema]
    is_entry_point: StrictBool = False
    is_finish_point: StrictBool = False


class ConditionalEdge(BaseModel):
    type: StrictStr = Field(
        default="conditional",
        allow_mutation=False,
    )

    source: StrictStr | list[StrictStr]
    intermediates: list[StrictStr]
    router: Callable[[StateSchema, ConfigSchema], StateSchema]


class SimpleEdge(BaseModel):
    type: StrictStr = Field(
        default="simple",
        allow_mutation=False,
    )

    source: StrictStr | list[StrictStr]
    target: StrictStr


class MultiAgentGraph(BaseModel):
    state_schema: Type[BaseModel]
    config_schema: Type[BaseModel]
    nodes: list[Node]
    edges: list[SimpleEdge | ConditionalEdge]
    with_memory: StrictBool = True
    graph: Type[StateGraph] | None = None

    def _add_nodes(self, graph_builder: StateGraph) -> None:
        for node in self.nodes:
            node_name = node.name
            graph_builder.add_node(node_name, node.run)

            if node.is_entry_point:
                graph_builder.set_entry_point(node_name)

            if node.is_finish_point:
                graph_builder.set_finish_point(node_name)

    def _add_edges(self, graph_builder: StateGraph) -> None:
        for edge in self.edges:
            if edge.type == "simple":
                graph_builder.add_edge(edge.source, edge.target)
                continue

            if edge.type == "conditional":
                graph_builder.add_conditional_edges(
                    edge.source,
                    edge.router,
                    edge.intermediates,
                )

                continue

    def compile(self) -> None:
        graph_builder = StateGraph(
            state_schema=self.state_schema,
            config_schema=self.config_schema,
        )

        self._add_nodes(graph_builder=graph_builder)
        self._add_edges(graph_builder=graph_builder)

        checkpointer = MemorySaver() if self.with_memory else None
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
        input_state: StateSchema,
        config: ConfigSchema,
        thread_id: str,
    ) -> BaseModel:
        config = {
            "configurable": {
                "thread_id": thread_id,
                **config.model_dump(),
            }
        }

        return await self.graph.ainvoke(input=input_state, config=config)
