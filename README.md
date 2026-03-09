# Multi Agents

`multi_agents` is a small Python toolkit for building multi-agent workflows on top of LangGraph.
It provides a thin typed wrapper around `StateGraph`, with Pydantic-based state/context schemas, node definitions, and simple or conditional edges.

## Setup

Run the project inside the devcontainer. Jupyter is available there for the notebooks in [`notebooks/`](./notebooks).

## Usage

The typical flow is:

1. Define a state schema and a context schema.
2. Create `Node` objects with `run` functions.
3. Connect nodes with `SimpleEdge` or `ConditionalEdge`.
4. Build a `MultiAgentGraph` and call `compile()`.
5. Execute it with `await graph.run(...)`.

Minimal example:

```python
import asyncio

from pydantic import BaseModel

from multi_agents.graph import MultiAgentGraph, Node


class State(BaseModel):
    text: str
    n_chars: int = 0


class Context(BaseModel):
    pass


def count_chars(state: State) -> dict[str, int]:
    return {"n_chars": len(state.text)}


counter = Node(
    name="counter",
    run=count_chars,
    is_entry_point=True,
    is_finish_point=True,
)

graph = MultiAgentGraph(
    state_schema=State,
    context_schema=Context,
    nodes=[counter],
    edges=[],
    with_memory=True,
)
graph.compile()


async def main() -> None:
    result = await graph.run(
        input_state=State(text="hello"),
        context=Context(),
        thread_id="example-thread",
    )
    print(result)


asyncio.run(main())
```

For a more complete example, see [`multi_agents/examples/simple_multi_agent/`](./multi_agents/examples/simple_multi_agent) and the notebook in [`notebooks/01-examples/01-simple-multi-agent.ipynb`](./notebooks/01-examples/01-simple-multi-agent.ipynb).

## Main components

- `multi_agents.graph.MultiAgentGraph`: wrapper around LangGraph compilation and execution.
- `multi_agents.graph.Node`: a named node with a sync or async `run` function.
- `multi_agents.graph.SimpleEdge`: direct transition from one node to another.
- `multi_agents.graph.ConditionalEdge`: transition decided by a router function.

For `ConditionalEdge`, the router receives the current state and returns the next destination or destinations. In practice, that means the router decides which node from `intermediates` should run next, or whether the graph should stop early, for example by returning `END`.

## Dependencies

The library depends mainly on:

- `langgraph`
- `pydantic`
- `ipython` for graph display helpers

It also uses the internal `common` package for logging.

## External installation

External projects can install `multi_agents` as a regular dependency.

For example, [`lupai`](https://github.com/aureka-team/lupai) uses it as a dependency.

In `requirements.txt`:

```txt
multi-agents>=<version>
```

In `uv.toml`:

```toml
[pip]
find-links = [
    "https://github.com/aureka-team/multi-agents/releases/expanded_assets/index",
]
```

## Releases

Pushing a Git tag matching `v*` creates a new release through [`.github/workflows/python-release.yml`](./.github/workflows/python-release.yml).

Example:

```bash
git tag v<version>
git push origin v<version>
```

The workflow builds the wheel, creates the GitHub release for the tag, and uploads the wheel to both the tag release and the permanent `index` release used by `uv`.

## Notebooks

Example notebooks are provided under [`notebooks/`](./notebooks):

- `01-examples`

## License

This project is licensed under the terms of the [`LICENSE`](./LICENSE) file.
