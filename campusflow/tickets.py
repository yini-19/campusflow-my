import random
import string
import json
import os

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


def save_ticket(ticket: dict):
    filename = "tickets.json"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            all_tickets = json.load(f)

            if isinstance(all_tickets, dict):
                all_tickets = [all_tickets]
    else:
        all_tickets = [] 
    
    all_tickets.append(ticket)
    
    with open(filename, "w") as f:
        json.dump(all_tickets, f, indent=4)

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
        
        save_ticket(ticket_dict)

        print("Processing ticket...")
        print("Ticket created")
        return ticket_dict

def list_tickets():
    all_tickets = []
    filename = "tickets.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            all_tickets = json.load(f)
        
        for ticket in all_tickets:
            #print(ticket)
            for key, value in ticket.items():
                print(f"{key}: {value}")
            print()
    else:
        print("No tickets found.")

def view_ticket():
    ticket_id = input("input ticket ID: ")
    all_tickets = []
    filename = "tickets.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            all_tickets = json.load(f)
        
        for ticket in all_tickets:
            if ticket["ID"] == ticket_id:
                for key, value in ticket.items():
                    print(f"{key}: {value}")
            print()
            
    else:
        print("No tickets found.")
    return

def assign_ticket():
    return

def workflow_status():
    return

def reports():
    return

def show_qeueu():
    return

while True:
    print("""
    =========================
        CAMPUS WORKFLOW
    =========================
        1. CREATE TICKET
        2. LIST ALL TICKETS
        3. VIEW TICKET
        4. ASSIGN TICKET TO STAFF
        5. STATUS(WORKFLOW)
        6. WORK QUEUE
        7. REPORTS
        8. EXIT
    """ )
    choice = input("Select action: ").strip()

    if choice == "1":
        create_ticket()
    elif choice == "2":
        list_tickets()
    elif choice == "3":
        view_ticket()
    elif choice == "4":
        assign_ticket()
    elif choice == "4":
         workflow_status()
    elif choice == "6":
         show_qeueu()
    elif choice == "7":
         reports()
    elif choice == "8":
        print("Good Bye!")
        break
    else:
        print("invalid choice, between options 1 to 6")


