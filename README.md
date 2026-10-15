# AeroCycle — Airport Runway Inspection Control

AeroCycle is an academic desktop simulation for managing repeated airport-area
inspection rounds. It demonstrates a manually implemented doubly circular linked
list using Python 3.11+, Tkinter, and ttk. It is not connected to aviation
systems and must not be used for real operational decisions.

## Academic purpose

The project makes the `next` and `prev` references visible through navigation,
the circular map, and the Data Structure Inspector. Moving forward from the
last sector returns to the first; moving backward from the first returns to the
last.

## Structure

- `sector.py`: the `RunwaySector` node, including its data and links.
- `inspection_circuit.py`: all linked-list operations and integrity checks.
- `interface.py`: Tkinter/ttk presentation and Canvas map.
- `main.py`: application entry point.
- `test_inspection_circuit.py`: standard-library `unittest` coverage.

The circuit is the only persistent collection of sectors. The interface asks
the circuit for traversals and never edits links directly.

## Run

```text
python main.py
```

Use **Load Demo Airport** to add six sectors individually through the public
insertion method. Use the management form to add, insert, update, find, or
delete sectors. The map is a visualization; the linked list remains the source
of truth.

## Test

```text
python -m unittest -v
```

The tests cover empty and singleton circuits, all insertion and deletion
positions, duplicate and invalid input, bidirectional wrap-around navigation,
inspection rounds, traversal termination, and pointer integrity:
`head.prev is tail`, `tail.next is head`, and reciprocal links for every node.

## Why a doubly circular linked list?

An inspection route repeats naturally. A circular list avoids a special
restart operation at the route boundaries, while `prev` supports reverse
rounds without rebuilding or reversing a collection. Each insertion or
deletion updates both neighboring links and preserves the invariants checked by
`validate_integrity()`.
