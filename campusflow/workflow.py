def assign_ticket(
    tickets: list[dict],
    ticket_id: str,
    staff_name: str,
) -> dict:
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["assigned_to"] = staff_name
            return ticket
    return ValueError(f"Ticket ID {ticket_id} not found")


def change_status(
    tickets: list[dict],
    ticket_id: str,
    new_status: str,
) -> dict:
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            current_status = ticket["status"]

            if current_status == "resolved":
                raise ValueError(
                    "Resolved tickets must be reopened first"
                )

            if new_status == "in_progress":
                if not ticket["assigned_to"]:
                    raise ValueError(
                        "Cannot start work on an unassigned ticket"
                    )

                if current_status != "open":
                    raise ValueError(
                        "Ticket must be open before work starts"
                    )

            if new_status == "resolved":
                if current_status != "in_progress":
                    raise ValueError(
                        "Only an in-progress ticket can be resolved"
                    )

            if new_status == "open":
                raise ValueError(
                    "Use reopen_ticket() to reopen a ticket"
                )

            ticket["status"] = new_status
            return ticket

    raise ValueError(f"Ticket '{ticket_id}' not found")


def reopen_ticket(
    tickets: list[dict],
    ticket_id: str,
) -> dict:
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            if ticket["status"] != "resolved":
                raise ValueError("Only resolved tickets can be reopened")

            ticket["status"] = "open"
            return ticket

    raise ValueError(f"Ticket '{ticket_id}' not found")  


def get_ticket(
    tickets: list[dict],
    ticket_id: str,
) -> dict:
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    raise ValueError(f"Ticket '{ticket_id}' not found")


def list_tickets(
    tickets: list[dict],
) -> list[dict]:
    return tickets

def get_work_queue(
    tickets: list[dict],
) -> list[dict]:
    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    unresolved_tickets = [
        ticket
        for ticket in tickets
        if ticket["status"] in ("open", "in_progress")
    ]

    return sorted(
        unresolved_tickets,
        key=lambda ticket: (
            priority_order[ticket["priority"]],
            int(ticket["id"][1:]),
        ),
    )