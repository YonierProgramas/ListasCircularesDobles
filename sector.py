class RunwaySector:
    """A sector stored in the inspection circuit."""

    def __init__(self, sector_id, name, sector_type, priority):
        self.sector_id = sector_id
        self.name = name
        self.sector_type = sector_type
        self.priority = priority
        self.status = "PENDING"
        self.observations = ""
        self.inspection_count = 0
        self.next = None
        self.prev = None

    def __repr__(self):
        return f"RunwaySector({self.sector_id!r})"
