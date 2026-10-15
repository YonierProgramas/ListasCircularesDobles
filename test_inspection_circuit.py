import unittest

from inspection_circuit import InspectionCircuit
from sector import RunwaySector


def make_sector(number):
    return RunwaySector(f"S-{number}", f"Sector {number}", "RUNWAY", "HIGH")


class InspectionCircuitTests(unittest.TestCase):
    def setUp(self):
        self.circuit = InspectionCircuit()

    def assert_valid(self):
        self.assertTrue(self.circuit.validate_integrity())
        if self.circuit.length:
            self.assertIs(self.circuit.head.prev, self.circuit.tail)
            self.assertIs(self.circuit.tail.next, self.circuit.head)
            for sector in self.circuit.traverse_forward():
                self.assertIs(sector.next.prev, sector)
                self.assertIs(sector.prev.next, sector)

    def test_empty_and_singleton_circuit(self):
        self.assert_valid()
        self.circuit.insert_at_end(make_sector(1))
        self.assertIs(self.circuit.head.next, self.circuit.head)
        self.assertIs(self.circuit.head.prev, self.circuit.head)
        self.assert_valid()

    def test_insertions_and_traversal(self):
        self.circuit.insert_at_end(make_sector(2))
        self.circuit.insert_at_beginning(make_sector(1))
        self.circuit.insert_at_end(make_sector(4))
        self.circuit.insert_at_position(make_sector(3), 2)
        self.assertEqual([s.sector_id for s in self.circuit.traverse_forward()],
                         ["S-1", "S-2", "S-3", "S-4"])
        self.assertEqual([s.sector_id for s in self.circuit.traverse_backward()],
                         ["S-4", "S-3", "S-2", "S-1"])
        self.assert_valid()

    def test_invalid_positions_and_duplicate_ids(self):
        self.circuit.insert_at_end(make_sector(1))
        with self.assertRaises(ValueError):
            self.circuit.insert_at_position(make_sector(2), -1)
        with self.assertRaises(ValueError):
            self.circuit.insert_at_position(make_sector(2), 2)
        with self.assertRaises(ValueError):
            self.circuit.insert_at_end(make_sector(1))

    def test_deletions_and_navigation_wrap(self):
        for number in (1, 2, 3):
            self.circuit.insert_at_end(make_sector(number))
        self.circuit.move_to_sector("S-3")
        self.assertEqual(self.circuit.move_next().sector_id, "S-1")
        self.assertEqual(self.circuit.move_previous().sector_id, "S-3")
        self.circuit.delete_sector("S-1")
        self.circuit.delete_sector("S-2")
        self.assertEqual(self.circuit.length, 1)
        self.circuit.delete_sector("S-3")
        self.assert_valid()

    def test_update_inspection_reset_and_complete_round(self):
        self.circuit.insert_at_end(make_sector(1))
        self.circuit.insert_at_end(make_sector(2))
        self.circuit.update_sector("S-1", name="Updated", observations="Clear")
        self.assertEqual(self.circuit.find_sector("S-1").name, "Updated")
        self.circuit.start_inspection_round()
        self.circuit.mark_inspected()
        self.circuit.move_next()
        self.circuit.mark_inspected()
        self.assertTrue(self.circuit.complete_round())
        self.assertEqual(self.circuit.rounds_completed, 1)
        self.circuit.reset_inspection_round()
        self.assertEqual(self.circuit.count_status("PENDING"), 2)

    def test_clear_and_missing_sector(self):
        self.circuit.insert_at_end(make_sector(1))
        with self.assertRaises(KeyError):
            self.circuit.delete_sector("missing")
        self.circuit.clear_circuit()
        self.assertEqual(self.circuit.length, 0)
        self.assert_valid()


if __name__ == "__main__":
    unittest.main()
