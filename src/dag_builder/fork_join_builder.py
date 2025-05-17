import random
from typing import Generator, List

import networkx as nx

from ..common import Util
from ..config import Config
from ..exceptions import BuildFailedError, InfeasibleConfigError
from .dag_builder_base import DAGBuilderBase


class ForkJoinBuilder(DAGBuilderBase):
    """Generates fork-join structured DAGs where each fork leads to a matching join."""

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self._max_fork_depth = (
            max(config.fork_depth) if isinstance(config.fork_depth, list) else config.fork_depth
        )
        self._max_fork = (
            max(config.nr_fork) if isinstance(config.nr_fork, list) else config.nr_fork
        )

    def _validate_config(self, config: Config):
        number_of_source_nodes = Util.get_option_min(config.number_of_source_nodes) or 1
        number_of_sink_nodes = Util.get_option_min(config.number_of_sink_nodes) or 1
        number_of_nodes = Util.get_option_max(config.number_of_nodes)
        if number_of_source_nodes + number_of_sink_nodes > number_of_nodes:
            raise InfeasibleConfigError(
                "'Number of source nodes' + 'Number of sink nodes' > 'Number of nodes'"
            )

    def build(self) -> Generator:
        """Build a DAG using recursive fork-join pattern."""
        for _ in range(self._config.number_of_dags):
            G = nx.DiGraph()
            node_counter = [0]  # Mutable integer for unique node IDs

            def next_node_id():
                node_counter[0] += 1
                return node_counter[0]

            def recursive_fork_join(entry: int, depth: int) -> int:
                if depth == 0:
                    return entry  # Base case: return this as a leaf

                # Fork into children
                num_forks = random.randint(2, self._max_fork)
                children = []
                for _ in range(num_forks):
                    child = next_node_id()
                    G.add_node(child)
                    G.add_edge(entry, child)
                    children.append(child)

                # Recursively process each child
                leaf_nodes = [recursive_fork_join(child, depth - 1) for child in children]

                # Create join node
                join_node = next_node_id()
                G.add_node(join_node)
                for leaf in leaf_nodes:
                    G.add_edge(leaf, join_node)

                return join_node  # Return join as output of this level

            # Create entry node
            entry_node = 0
            G.add_node(entry_node)

            final_output = recursive_fork_join(entry_node, self._max_fork_depth)

            # Optional: Add final sink node
            if self._config.number_of_sink_nodes:
                num_sinks = Util.random_choice(self._config.number_of_sink_nodes)
                for _ in range(num_sinks):
                    sink = next_node_id()
                    G.add_node(sink)
                    G.add_edge(final_output, sink)

            yield G
