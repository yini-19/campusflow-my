
from campusflow.tickets import (
    display_menu,
    create_ticket,
    list_tickets,
    view_ticket
)


def main():
    while True:
        display_menu()
        choice = input("Select action: ").strip()

        if choice == "1":
            create_ticket()
        elif choice == "2":
            list_tickets()
        elif choice == "3":
            view_ticket()
        elif choice == "4":
            assign_ticket()
        elif choice == "5":
            workflow_status()
        elif choice == "6":
            show_qeueu()
        elif choice == "7":
            reports()
        elif choice == "8":
            print("Good Bye!")
            break
        else:
            print("Invalid choice. Select an option between 1 and 8.")


if __name__ == "__main__":
    main()