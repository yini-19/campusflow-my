import json

def load_tickets(path: str) -> list[dict]:
    try:
        with open(path, "r") as f:
            tickets = json.load(f)
            f.close()
            return tickets
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        raise ValueError(f"Malformed JSON in {path}")
    except Exception as e:
        raise e

def save_tickets(tickets: list[dict], path: str) -> None:
    with open(path, "w") as f:
        json.dump(tickets, f, indent=4)
        f.close()


def generate_ticket_id(tickets: list[dict]) -> str:
    if not tickets:
        return "TICKET-1"
    ticket_ids = [int(ticket["id"].split("-")[1]) for ticket in tickets]
    new_id = max(ticket_ids) + 1
    return f"TICKET-{new_id}"