# Ticket Tracker

A lightweight Python ticket management system featuring JSON serialization, status/priority validation, and user assignment.

---

## Features

* **Ticket Management:** Create, retrieve, update statuses, assign users, and delete tickets.
* **Validation:** Automatic checks for valid statuses (`open`, `in_progress`, `closed`) and priorities (`low`, `medium`, `high`).
* **Persistence:** Save and load ticket tracker states to and from JSON files.
* **Filtering:** Easily fetch all active tickets (`open` or `in_progress`).

---

## Class Structure

* `User`: Represents a system user/assignee.
* `Ticket`: Data class representing a ticket with built-in validation and dictionary serialization.
* `TicketTracker`: Main manager for storing, modifying, loading, and saving tickets.
* `TicketNotFoundError`: Exception raised when accessing a non-existent ticket ID.

---

## Usage Example

```python
from main import TicketTracker, User

# Initialize the tracker
tracker = TicketTracker()

# Create tickets
tracker.create_ticket("Fix authentication bug", priority="high", description="500 error on login")
tracker.create_ticket("Update documentation", priority="low")

# Assign a ticket to a user
dev = User("Alex")
tracker.assign_ticket(ticket_id=1, user=dev)

# Update ticket status
tracker.change_status(ticket_id=1, status="in_progress")

# Get active tickets
active_tickets = tracker.get_open_tickets()

# Save state to JSON
tracker.save("tickets.json")

# Load state from JSON
loaded_tracker = TicketTracker.load("tickets.json")

```

---

## Requirements

* Python 3.10+ (uses modern union type hints like `User | None`).
