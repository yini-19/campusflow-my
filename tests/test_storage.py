
import json
import tempfile
import unittest
from pathlib import Path

from campusflow.tickets import create_ticket
from campusflow.storage import (
    generate_ticket_id,
    load_tickets,
    save_tickets,
)


class TicketStorageTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.path = str(
            Path(self.temp_dir.name) / "tickets.json"
        )

        self.tickets = [
            create_ticket(
                title="Network unavailable",
                category="Network",
                urgency="high",
                affected_users=12,
                ticket_id="T001",
            ),
            create_ticket(
                title="Laptop issue",
                category="Hardware",
                urgency="low",
                affected_users=1,
                ticket_id="T002",
            ),
        ]

    def test_save_and_reload_preserves_tickets(self):
        save_tickets(self.tickets, self.path)

        reloaded = load_tickets(self.path)

        self.assertEqual(reloaded, self.tickets)

    def test_ticket_created_after_reload_gets_unique_id(self):
        save_tickets(self.tickets, self.path)
        reloaded = load_tickets(self.path)

        new_id = generate_ticket_id(reloaded)

        self.assertEqual(new_id, "T003")
        self.assertNotIn(
            new_id,
            [ticket["id"] for ticket in reloaded],
        )

    def test_missing_file_returns_empty_list(self):
        missing_path = str(
            Path(self.temp_dir.name) / "missing.json"
        )

        self.assertEqual(load_tickets(missing_path), [])

    def test_corrupted_json_raises_value_error(self):
        with open(self.path, "w", encoding="utf-8") as file:
            file.write("{not valid JSON")

        with self.assertRaisesRegex(
            ValueError,
            "Malformed JSON",
        ):
            load_tickets(self.path)

    def test_duplicate_ticket_ids_are_rejected(self):
        duplicated_tickets = [
            self.tickets[0],
            self.tickets[0],
        ]

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(duplicated_tickets, file)

        with self.assertRaisesRegex(
            ValueError,
            "Duplicate ticket ID",
        ):
            load_tickets(self.path)

    def test_non_list_json_is_rejected(self):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump({"id": "T001"}, file)

        with self.assertRaisesRegex(
            ValueError,
            "expected a list of tickets",
        ):
            load_tickets(self.path)

    def test_id_generation_handles_a_gap_in_existing_ids(self):
        tickets = [
            {"id": "T001"},
            {"id": "T003"},
        ]

        self.assertEqual(generate_ticket_id(tickets), "T004")


if __name__ == "__main__":
    unittest.main()