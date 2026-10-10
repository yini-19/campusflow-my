
import json
import re


def load_tickets(path: str) -> list[dict]:
    try:
        with open(path, "r", encoding="utf-8") as file:
            tickets = json.load(file)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Malformed JSON in {path}: {exc}"
        ) from exc

    if not isinstance(tickets, list):
        raise ValueError(
            f"Invalid data in {path}: expected a list of tickets"
        )

    seen_ids = set()

    for index, ticket in enumerate(tickets):
        if not isinstance(ticket, dict):
            raise ValueError(
                f"Invalid ticket at position {index}: "
                "expected a dictionary"
            )

        ticket_id = ticket.get("id")

        if not isinstance(ticket_id, str) or not ticket_id.strip():
            raise ValueError(
                f"Invalid ticket at position {index}: "
                "missing or invalid ID"
            )

        if ticket_id in seen_ids:
            raise ValueError(
                f"Duplicate ticket ID found: {ticket_id}"
            )

        seen_ids.add(ticket_id)

    return tickets


def save_tickets(
    tickets: list[dict],
    path: str,
) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)


def generate_ticket_id(tickets: list[dict]) -> str:
    highest_number = 0

    for ticket in tickets:
        match = re.fullmatch(r"T(\d+)", ticket["id"])

        if match:
            highest_number = max(
                highest_number,
                int(match.group(1)),
            )

    return f"T{highest_number + 1:03d}"