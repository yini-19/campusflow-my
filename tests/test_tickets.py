
import json
import os
import unittest
from unittest.mock import patch

from campusflow import tickets


class TestCreateTicket(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_tickets.json"
        self.original_filename = tickets.FILENAME if hasattr(
            tickets, "FILENAME"
        ) else None

    
        self.filename_patcher = patch.object(
            tickets, "FILENAME", self.test_file, create=True
        )
        self.filename_patcher.start()

        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        self.filename_patcher.stop()

        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @patch("builtins.input", side_effect=[
        "Campus Wi-Fi is down", "Network", "high", "15"
    ])
    def test_create_ticket_success(self, mock_input):
        ticket = tickets.create_ticket()

        self.assertEqual(ticket["ID"], "T001")
        self.assertEqual(ticket["Title"], "Campus Wi-Fi is down")
        self.assertEqual(ticket["Category"], "Network")
        self.assertEqual(ticket["Urgency"], "high")
        self.assertEqual(ticket["Affected_users"], 15)
        self.assertEqual(ticket["Priority"], "critical")
        self.assertEqual(ticket["Status"], "open")
        self.assertIsNone(ticket["Assigned_to"])

    @patch("builtins.input", side_effect=[
        "", "Valid title", "Network", "high", "15"
    ])
    def test_create_ticket_retries_blank_title(self, mock_input):
        ticket = tickets.create_ticket()

        self.assertEqual(ticket["Title"], "Valid title")
        self.assertEqual(mock_input.call_count, 5)

    @patch("builtins.input", side_effect=[
        "Laptop issue", "InvalidCategory", "Hardware", "medium", "5"
    ])
    def test_create_ticket_retries_invalid_category(self, mock_input):
        ticket = tickets.create_ticket()

        self.assertEqual(ticket["Category"], "Hardware")
        self.assertEqual(mock_input.call_count, 5)

    @patch("builtins.input", side_effect=[
        "Software issue", "Software", "urgent", "low", "2"
    ])
    def test_create_ticket_retries_invalid_urgency(self, mock_input):
        ticket = tickets.create_ticket()

        self.assertEqual(ticket["Urgency"], "low")
        self.assertEqual(mock_input.call_count, 5)

    @patch("builtins.input", side_effect=[
        "Broken laptop", "Hardware", "high", "0", "4"
    ])
    def test_create_ticket_retries_invalid_affected_users(self, mock_input):
        ticket = tickets.create_ticket()

        self.assertEqual(ticket["Affected_users"], 4)
        self.assertEqual(mock_input.call_count, 5)

    @patch("builtins.input", side_effect=[
        "Network problem", "Network", "medium", "3"
    ])
    def test_create_ticket_saves_to_json(self, mock_input):
        ticket = tickets.create_ticket()

        with open(self.test_file, "r", encoding="utf-8") as file:
            saved_tickets = json.load(file)

        self.assertEqual(len(saved_tickets), 1)
        self.assertEqual(saved_tickets[0]["ID"], ticket["ID"])

    @patch("builtins.input", side_effect=[
        "First issue", "Software", "low", "1",
        "Second issue", "Hardware", "high", "10"
    ])
    def test_create_ticket_generates_unique_ids(self, mock_input):
        first = tickets.create_ticket()
        second = tickets.create_ticket()

        self.assertEqual(first["ID"], "T001")
        self.assertEqual(second["ID"], "T002")


class TestListTickets(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_tickets.json"
        self.filename_patcher = patch.object(
            tickets, "FILENAME", self.test_file, create=True
        )
        self.filename_patcher.start()

        self.sample_tickets = [
            {
                "ID": "T001",
                "Title": "Wi-Fi issue",
                "Category": "Network",
                "Urgency": "high",
                "Affected_users": 15,
                "Priority": "critical",
                "Status": "open",
                "Assigned_to": None,
            }
        ]

    def tearDown(self):
        self.filename_patcher.stop()

        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @patch("builtins.print")
    def test_list_tickets_displays_saved_ticket(self, mock_print):
        with open(self.test_file, "w", encoding="utf-8") as file:
            json.dump(self.sample_tickets, file)

        tickets.list_tickets()

        printed_text = " ".join(
        str(arg)
        for call in mock_print.call_args_list
        for arg in call.args
    )
        self.assertIn("Wi-Fi issue", printed_text)
        self.assertIn("T001", printed_text)

    @patch("builtins.print")
    def test_list_tickets_when_file_missing(self, mock_print):
        tickets.list_tickets()

        mock_print.assert_any_call("No tickets found.")

    @patch("builtins.print")
    def test_list_tickets_displays_multiple_tickets(self, mock_print):
        second_ticket = dict(self.sample_tickets[0])
        second_ticket["ID"] = "T002"
        second_ticket["Title"] = "Laptop issue"

        with open(self.test_file, "w", encoding="utf-8") as file:
            json.dump(self.sample_tickets + [second_ticket], file)

        tickets.list_tickets()

        printed_text = " ".join(
        str(arg)
        for call in mock_print.call_args_list
        for arg in call.args
    )
        self.assertIn("Wi-Fi issue", printed_text)
        self.assertIn("Laptop issue", printed_text)


class TestViewTicket(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_tickets.json"
        self.filename_patcher = patch.object(
            tickets, "FILENAME", self.test_file, create=True
        )
        self.filename_patcher.start()

        self.sample_ticket = {
            "ID": "T001",
            "Title": "Wi-Fi issue",
            "Category": "Network",
            "Urgency": "high",
            "Affected_users": 15,
            "Priority": "critical",
            "Status": "open",
            "Assigned_to": None,
        }

        with open(self.test_file, "w", encoding="utf-8") as file:
            json.dump([self.sample_ticket], file)

    def tearDown(self):
        self.filename_patcher.stop()

        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @patch("builtins.print")
    @patch("builtins.input", return_value="T001")
    def test_view_ticket_displays_existing_ticket(
        self, mock_input, mock_print
    ):
        tickets.view_ticket()

        printed_text = " ".join(
        str(arg)
        for call in mock_print.call_args_list
        for arg in call.args
    )
        self.assertIn("Wi-Fi issue", printed_text)
        self.assertIn("T001", printed_text)

    @patch("builtins.print")
    @patch("builtins.input", return_value="T999")
    def test_view_ticket_displays_not_found(
        self, mock_input, mock_print
    ):
        tickets.view_ticket()

        mock_print.assert_any_call("Ticket not found.")

    @patch("builtins.print")
    @patch("builtins.input", return_value="t001")
    def test_view_ticket_accepts_lowercase_id(
        self, mock_input, mock_print
    ):
        tickets.view_ticket()

        printed_text = " ".join(
        str(arg)
        for call in mock_print.call_args_list
        for arg in call.args
    )
        self.assertIn("Wi-Fi issue", printed_text)


if __name__ == "__main__":
    unittest.main()