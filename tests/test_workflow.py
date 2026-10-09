
import unittest

from campusflow.workflow import (
    assign_ticket,
    change_status,
    get_ticket,
    get_work_queue,
    reopen_ticket,
)


class TicketWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "title": "Network unavailable",
                "category": "Network",
                "urgency": "high",
                "affected_users": 12,
                "priority": "critical",
                "status": "open",
                "assigned_to": "",
            },
            {
                "id": "T002",
                "title": "Laptop issue",
                "category": "Hardware",
                "urgency": "low",
                "affected_users": 1,
                "priority": "low",
                "status": "open",
                "assigned_to": "",
            },
            {
                "id": "T010",
                "title": "Application error",
                "category": "Software",
                "urgency": "low",
                "affected_users": 4,
                "priority": "medium",
                "status": "open",
                "assigned_to": "",
            },
            {
                "id": "T003",
                "title": "Email issue",
                "category": "Software",
                "urgency": "high",
                "affected_users": 2,
                "priority": "high",
                "status": "open",
                "assigned_to": "",
            },
        ]

    def test_unassigned_ticket_cannot_move_to_in_progress(self):
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "in_progress")

        self.assertEqual(
            get_ticket(self.tickets, "T001")["status"],
            "open",
        )

    def test_assigned_ticket_can_progress_to_resolved(self):
        assign_ticket(self.tickets, "T001", "Ada")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")

        ticket = get_ticket(self.tickets, "T001")
        self.assertEqual(ticket["status"], "resolved")
        self.assertEqual(ticket["assigned_to"], "Ada")

    def test_queue_sorts_by_priority_then_numeric_id(self):
        self.tickets.append(
            {
                "id": "T020",
                "title": "Another urgent issue",
                "category": "Network",
                "urgency": "high",
                "affected_users": 2,
                "priority": "high",
                "status": "open",
                "assigned_to": "",
            }
        )

        queue_ids = [
            ticket["id"]
            for ticket in get_work_queue(self.tickets)
        ]

        self.assertEqual(
            queue_ids,
            ["T001", "T003", "T020", "T010", "T002"],
        )

    def test_resolved_ticket_is_excluded_from_queue(self):
        self.tickets[0]["status"] = "resolved"

        queue_ids = [
            ticket["id"]
            for ticket in get_work_queue(self.tickets)
        ]

        self.assertNotIn("T001", queue_ids)

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "pending")

    def test_unknown_ticket_id_is_rejected(self):
        with self.assertRaises(ValueError):
            get_ticket(self.tickets, "T999")

    def test_resolved_ticket_can_be_reopened(self):
        self.tickets[0]["status"] = "resolved"

        reopened = reopen_ticket(self.tickets, "T001")

        self.assertEqual(reopened["status"], "open")

    def test_resolved_ticket_cannot_be_assigned_without_reopening(self):
        self.tickets[0]["status"] = "resolved"

        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "Ada")

    def test_blank_staff_name_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "   ")


if __name__ == "__main__":
    unittest.main()