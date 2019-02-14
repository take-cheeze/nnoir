import heapq
import msgpack
import chainer
import numpy as np
from chainer import variable
from chainer import function_node
import chainer.functions as F
import mlir
from .patch import encode_ndarray


class Node(object):
    def __init__(self, node, no=None):
        self.no = no
        self.node = node
        self.in_edges = []
        self.out_edges = []

    def __hash__(self):
        return id(self.node).__hash__()

    def __eq__(self, r):
        return self.node is r.node

    def add_in_edge(self, from_node):
        self.in_edges.append(from_node)

    def add_out_edge(self, to_node):
        self.out_edges.append(to_node)

    def is_type_of(self, cls):
        return isinstance(self.node, cls)


class Graph(object):
    def __init__(self, model, input_variables, output_variables):
        self.input_variables = []
        self.output_variables = []
        self.nodes = set()
        self.model = model

        push_count = [0]
        candidates = []

        def add_candidate(candidate):
            heapq.heappush(candidates, (push_count[0], candidate))
            push_count[0] += 1

        n2N = {}
        created_order = [0]

        def create_node(node):
            if id(node) in n2N:
                return n2N[id(node)]
            else:
                n2N[id(node)] = Node(node, created_order[0])
                created_order[0] += 1
                return n2N[id(node)]

        out2link = {}
        for child in model.children():
            if hasattr(child, 'chainer_output_variables'):
                out2link.update({id(o): child for o in child.chainer_output_variables})

        # Create graph
        seen_edges = set()
        for o in output_variables:
            add_candidate(o)
            o_node = create_node(o)
            self.nodes.add(o_node)
            self.output_variables.append(o_node)
        while candidates:
            _, candidate = heapq.heappop(candidates)
            if isinstance(candidate, variable.Variable):
                creator = None
                if id(candidate) in out2link:
                    creator = out2link[id(candidate)]
                else:
                    creator = candidate.creator
                if hasattr(creator, 'caller') and creator.caller is not None:
                    creator = creator.caller
                if creator is None and id(candidate) not in map(id, input_variables):  # Constant Param
                    class Constant:
                        def __init__(self, value):
                            self.value = value

                        def to_mlir_node(self, inputs, outputs):
                            return mlir.functions.Constant(inputs, outputs, value=encode_ndarray(self.value))
                    creator = Constant(candidate.data)
                if creator is not None and (id(creator), id(candidate)) not in seen_edges:
                    add_candidate(creator)
                    seen_edges.add((id(creator), id(candidate)))
                    creator_node = create_node(creator)
                    candidate_node = create_node(candidate)
                    candidate_node.add_in_edge(creator_node)
                    creator_node.add_out_edge(candidate_node)
                    self.nodes.add(creator_node)
            else:
                if hasattr(candidate, 'chainer_input_variables'):
                    for input_ in reversed(candidate.chainer_input_variables):
                        if input_ is not candidate and (id(input_), id(candidate)) not in seen_edges:
                            add_candidate(input_)
                            seen_edges.add((id(input_), id(candidate)))
                            input_node = create_node(input_)
                            candidate_node = create_node(candidate)
                            candidate_node.add_in_edge(input_node)
                            input_node.add_out_edge(candidate_node)
                            self.nodes.add(input_node)
        for i in input_variables:
            self.input_variables.append(create_node(i))

        # Topological sorting
        visited = set()
        sorted_nodes = []

        def visit(node):
            if node not in visited:
                visited.add(node)
                if node.out_edges is not None:
                    for n in node.out_edges:
                        visit(n)
                sorted_nodes.insert(0, node)
        for node in sorted(self.nodes, key=lambda n: n.no):
            visit(node)
        for no, node in enumerate(sorted_nodes):
            node.no = no

    def to_mlir(self, name=None):

        def _value(node):
            return mlir.Value(_variable_elem_name(node), node.node.dtype.str, node.node.shape)

        def _function(node):
            return node.node.to_mlir_node(
                list(map(_variable_elem_name, reversed(node.in_edges))),
                list(map(_variable_elem_name, node.out_edges))
            )

        sorted_nodes = sorted(self.nodes, key=lambda n: n.no)

        return mlir.MLIR(
            (name or self.model.__class__.__name__).encode(),
            b'chainer',
            chainer.__version__,
            list(map(_variable_elem_name, self.input_variables)),
            list(map(_variable_elem_name, self.output_variables)),
            list(map(_value, filter(lambda node: isinstance(node.node, variable.Variable), sorted_nodes))),
            list(map(_function, filter(lambda node: not isinstance(node.node, variable.Variable), sorted_nodes)))
        ).pack()


def _variable_elem_name(node):
    return 'v{:d}'.format(node.no).encode()
