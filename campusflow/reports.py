def generate_report(
    tickets: list[dict],
) -> dict:
    report = {
        "total_tickets": len(tickets),
        "open_tickets": len([ticket for ticket in tickets if ticket["status"] == "open"]),
        "closed_tickets": len([ticket for ticket in tickets if ticket["status"] == "closed"]),
    }
    return report
