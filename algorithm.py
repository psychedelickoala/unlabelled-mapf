from data_structures.linked_list import LinkedList

class DemandNode:
    def __init__(self, label: int, parent: "DemandNode | None" = None, has_agent: bool = False, has_target: bool = False) -> None:
        self.has_agent: bool = has_agent
        self.has_target: bool = has_target
        self.demand: int = 0  # d(u)
        self.start: int = 0  # s(u)
        self.leaving: LinkedList[int] = LinkedList()  # l(u)
        self.neg_children: list[DemandNode] = []
        self.zero_children: list[DemandNode] = []
        self.pos_children: list[DemandNode] = []
        self.parent: DemandNode | None = parent
        self.processed = False
        self.label: int = label



class DemandTree:
    def __init__(self) -> None:
        self.moves: list[list[tuple[DemandNode, DemandNode]]] = []
        self.root: DemandNode = DemandNode()

    def build_from_tree(self):
        pass

    def process_subtree(self, u: DemandNode) -> None:
        if u.has_agent:
            u.leaving.insert(index = 0, item = u.start)  # insert s(u) at start of l(u)
        for v in u.neg_children:
            v.start = max(u.start - 1, u.leaving.get_last_item(), 0)
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
            return idx  # leave agent where it is

        
    def output_move(self, from_node: DemandNode, to_node: DemandNode, t: int) -> None:
        while t > len(self.moves) - 1:  # lengthen moves list until last index is t
            self.moves.append([])
        self.moves[t].append((from_node, to_node))
    
