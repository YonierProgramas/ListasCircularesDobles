from sector import RunwaySector


class InspectionCircuit:
    """Manual doubly circular linked list for airport inspection sectors."""

    def __init__(self):
        self.head = None
        self.current = None
        self.tail = None
        self.length = 0
        self.round_active = False
        self.rounds_completed = 0

    def _ensure_sector(self, sector):
        if not isinstance(sector, RunwaySector):
            raise TypeError("sector must be a RunwaySector")
        if self.find_sector(sector.sector_id) is not None:
            raise ValueError(f"Sector ID already exists: {sector.sector_id}")

    def insert_at_beginning(self, sector):
        self._ensure_sector(sector)
        if self.head is None:
            sector.next = sector.prev = sector
            self.head = self.tail = self.current = sector
        else:
            sector.next = self.head
            sector.prev = self.tail
            self.tail.next = sector
            self.head.prev = sector
            self.head = sector
        self.length += 1
        return sector

    def insert_at_end(self, sector):
        self._ensure_sector(sector)
        if self.head is None:
            return self.insert_at_beginning(sector)
        sector.prev = self.tail
        sector.next = self.head
        self.tail.next = sector
        self.head.prev = sector
        self.tail = sector
        self.length += 1
        return sector

    def insert_at_position(self, sector, position):
        """Insert at a zero-based position, including position ``length``."""
        if not isinstance(position, int) or isinstance(position, bool):
            raise ValueError("Position must be an integer")
        if position < 0 or position > self.length:
            raise ValueError("Position must be between 0 and the circuit length")
        if position == 0:
            return self.insert_at_beginning(sector)
        if position == self.length:
            return self.insert_at_end(sector)
        self._ensure_sector(sector)
        after = self._node_at(position)
        before = after.prev
        sector.prev = before
        sector.next = after
        before.next = sector
        after.prev = sector
        self.length += 1
        return sector

    def _node_at(self, position):
        if self.head is None or position < 0 or position >= self.length:
            raise IndexError("Position is outside the circuit")
        node = self.head
        for _ in range(position):
            node = node.next
        return node

    def delete_sector(self, sector_id):
        node = self.find_sector(sector_id)
        if node is None:
            raise KeyError(f"Sector not found: {sector_id}")
        if self.length == 1:
            self.head = self.current = self.tail = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if node is self.head:
                self.head = node.next
            if node is self.tail:
                self.tail = node.prev
            if node is self.current:
                self.current = node.next
        node.next = node.prev = None
        self.length -= 1
        if self.length == 0:
            self.round_active = False
        return node

    def find_sector(self, sector_id):
        if self.head is None:
            return None
        node = self.head
        for _ in range(self.length):
            if node.sector_id == sector_id:
                return node
            node = node.next
        return None

    def move_next(self):
        if self.current is None:
            return None
        self.current = self.current.next
        return self.current

    def move_previous(self):
        if self.current is None:
            return None
        self.current = self.current.prev
        return self.current

    def move_to_sector(self, sector_id):
        node = self.find_sector(sector_id)
        if node is None:
            raise KeyError(f"Sector not found: {sector_id}")
        self.current = node
        return node

    def traverse_forward(self):
        return self._traverse("next")

    def traverse_backward(self):
        start = self.tail
        result = []
        node = start
        for _ in range(self.length):
            result.append(node)
            node = node.prev
        return result

    def _traverse(self, direction):
        result = []
        node = self.head
        for _ in range(self.length):
            result.append(node)
            node = getattr(node, direction)
        return result

    def update_sector(self, sector_id, name=None, sector_type=None,
                      priority=None, status=None, observations=None):
        sector = self.find_sector(sector_id)
        if sector is None:
            raise KeyError(f"Sector not found: {sector_id}")
        if name is not None:
            sector.name = name
        if sector_type is not None:
            sector.sector_type = sector_type
        if priority is not None:
            sector.priority = priority
        if status is not None:
            if status not in ("PENDING", "INSPECTED", "REVIEW"):
                raise ValueError("Invalid sector status")
            sector.status = status
        if observations is not None:
            sector.observations = observations
        return sector

    def mark_inspected(self):
        if self.current is None:
            raise ValueError("There is no current sector")
        self.current.status = "INSPECTED"
        self.current.inspection_count += 1
        return self.current

    def reset_inspection_round(self):
        for sector in self.traverse_forward():
            sector.status = "PENDING"
        self.round_active = True

    def start_inspection_round(self):
        self.reset_inspection_round()

    def complete_round(self):
        if self.length and all(sector.status == "INSPECTED"
                               for sector in self.traverse_forward()):
            self.rounds_completed += 1
            self.round_active = False
            return True
        return False

    def clear_circuit(self):
        node = self.head
        for _ in range(self.length):
            following = node.next
            node.next = node.prev = None
            node = following
        self.head = self.current = self.tail = None
        self.length = 0
        self.round_active = False

    def validate_integrity(self):
        if self.length == 0:
            return self.head is None and self.current is None and self.tail is None
        if self.head is None or self.tail is None or self.current is None:
            return False
        if self.head.prev is not self.tail or self.tail.next is not self.head:
            return False
        node = self.head
        for _ in range(self.length):
            if node is None or node.next is None or node.prev is None:
                return False
            if node.next.prev is not node or node.prev.next is not node:
                return False
            node = node.next
        return node is self.head

    def count_status(self, status):
        return sum(1 for sector in self.traverse_forward()
                   if sector.status == status)

    def total_inspections(self):
        return sum(sector.inspection_count for sector in self.traverse_forward())
