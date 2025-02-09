import networkx as nx
#from time import time

class DemandNode:
    def __init__(self, label: int, parent: "DemandNode | None" = None, has_agent: bool = False, has_target: bool = False) -> None:
        self.has_agent: bool = has_agent
        self.has_target: bool = has_target
        self.demand: int = 0  # d(u)
        self.start: int = 0  # s(u)
        self.leaving: list[int] = []  # l(u)
        self.neg_children: list[DemandNode] = []
        self.zero_children: list[DemandNode] = []
        self.pos_children: list[DemandNode] = []
        self.parent: DemandNode | None = parent
        self.processed = False
        self.label: int = label

    def __str__(self) -> str:
        return f"{self.label}: d = {self.demand}"



class DemandTree:
    def __init__(self, G: nx.Graph, agents: list, targets: list) -> None:
        # set up agents, targets for O(1) lookup in build
        self.agent = [False]*len(G)
        self.target = [False]*len(G)
        for a in agents:
            self.agent[a] = True
        for t in targets:
            self.target[t] = True
        
        self.num_of_moves = 0
        #self.moves: list[dict[int, int]] = []
        self.root = DemandNode(0, has_agent=self.agent[0], has_target=self.target[0])
        
        # build tree
        self.initial_demands = [0]*len(G)
        self.visited = [False]*len(G)
        self.graph: nx.Graph = G
        self.build_demand(0, self.root)
        #self.build_demand_time = end - start
        #self.sum_of_costs = 0

        #self.reached: dict[int, int] = dict()  # the time each target is reached

        #start = time()
        #self.process_subtree(self.root)
        #end = time()
        #self.alg_time = end - start
        #self.makespan = len(self.moves)

    def build_demand(self, label: int, u: DemandNode) -> None:
        self.visited[label] = True
        u.demand = 0
        if self.agent[label]:
            u.demand -= 1
        if self.target[label]:
            u.demand += 1
        
        # process children
        for v in self.graph[label]:
            if not self.visited[v]:
                v_node = DemandNode(v, parent=u, has_agent=self.agent[v], has_target=self.target[v])  # O(1)
                self.build_demand(v, v_node)
                u.demand += v_node.demand
                # if v_node.demand < 0:
                #     u.neg_children.append(v_node)
                # elif v_node.demand == 0:
                #     u.zero_children.append(v_node)
                # else:
                #     u.pos_children.append(v_node)

        

    def process_subtree(self, u: DemandNode) -> None:
        if u.has_agent:
            u.leaving.insert(0, u.start)  # insert s(u) at start of l(u)
        for v in u.neg_children:
            v.start = max(u.start - 1, u.leaving[-1], 0)
            self.process_subtree(v)
            # demand of v should now be 0
        idx = 0
        for t in u.leaving:
            idx = self.process_agent(u, t, idx)
        u.processed = True
        for v in u.zero_children:
            self.process_subtree(v)
        for v in u.pos_children:
            self.process_subtree(v)
        
    def process_agent(self, u: DemandNode, t: int, idx: int) -> int:
        if u.demand < 0:
            assert u.parent is not None
            u.parent.leaving.append(t+1)
            self.output_move(u, u.parent, t)
            u.demand += 1
            return 0
        elif idx < len(u.pos_children):
            v = u.pos_children[idx]
            v.leaving.append(t+1)
            self.output_move(u, v, t)
            v.demand -= 1
            if v.demand == 0:
                return idx + 1
            else:
                return idx
        else:
            #self.sum_of_costs += t
            #self.reached[u.label] = t
            return idx  # leave agent where it is, it is at a target


        
    def output_move(self, from_node: DemandNode, to_node: DemandNode, t: int) -> None:
        self.num_of_moves += 1
        #while t > len(self.moves) - 1:  # lengthen moves list until last index is t
        #    self.moves.append(dict())
        #self.moves[t][from_node.label] = to_node.label
    
