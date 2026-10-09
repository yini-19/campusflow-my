import random
import string
import json

ticket_dict = {}

def validate_title() -> str:
    title = input("Ticket title: ").strip()
    if not title:
        print("Title field must not be empty")
    return title

def validate_category() -> str:
    try:
        category = input("Select category(Network, Software, Hardware, Facility, Other): ").capitalize()
    except ValueError:
        print("unsoppurted category: field cannot be empty")
    return category

def validate_urgency() -> str:
    try:
        urgency  = input("Urgency level of complaint(high, medium or low): ").lower()
    except ValueError:
        print("field cannot be empty")
    return urgency

def validate_affected_users() -> int:
    affected_users = input("Number of affected users: ")
    if affected_users.isdigit() and int(affected_users) > 0:
        return int(affected_users)
    else:
        raise ValueError("Entry must be a positive integer and must be greater than 0")
        
def calculate_priority(urgency: str, affected_users: int) -> str:
    if urgency == "high" and affected_users >= 10:
        priority = "critical"
        return priority
    elif urgency == "high" or affected_users >= 10:
        priority = "high"
        return priority
    elif urgency == "medium" or affected_users >= 3:
        priority = "medium"
        return priority
    else:
        priority = "low"
        return priority
    
def create_ticket() -> dict:
    ticket_id = "".join(random.choices(string.ascii_letters+string.digits, k=8))
    title = validate_title()
    category =validate_category()
    urgency = validate_urgency()
    affected_users = validate_affected_users()
    priority = calculate_priority(urgency, affected_users)

    global ticket_dict
    ticket_dict = {
        "ID":ticket_id,
        "Title": title,
        "Category": category,
        "Urgency": urgency,
        "Affected_users": affected_users,
        "Priority": priority,
        "Status": "open",
        "Assigned_to": None,
    }
    with open("tickets.json", "w") as f:
        json.dump(ticket_dict, f, indent=4)
    return ticket_dict
print(create_ticket())