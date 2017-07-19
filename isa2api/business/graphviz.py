from graphviz import Digraph


class Graphviz():
    def __init__(self, data):
        self.graph = Digraph('Test', format='svg')
        self.graph.attr('node', style="rounded,filled",
                        fontcolor="#FFF7F1", fontname="Arial")
        for node in data["nodes"]:
            if node["group"] == 'node':
                shape = 'box'
                fillcolor = "orange"
            else:
                shape = 'circle'
                fillcolor = "red"

            self.graph.node(
                node["id"], node["label"], shape=shape, fillcolor=fillcolor)
        for edge in data["edges"]:
            self.graph.edge(edge['from'], edge['to'],
                            edge['label'], penwidth=str(int(edge['value'] * 10) + 1))

    def svg(self):
        return self.graph.pipe().decode('utf-8').encode('utf-8')
