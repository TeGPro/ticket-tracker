from dataclasses import dataclass
import json

@dataclass
class User:
    name: str

@dataclass
class Ticket:
    id: int
    title: str
    _status: str
    _priority: str
    assigned_user: User | None = None
    
    def __post_init__(self) -> None:
        if self._status not in ['open', 'in_progress', 'closed']:
            raise ValueError
        if self._priority not in ['low', 'medium', 'high']:
            raise ValueError
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, status: str):
        if status not in ['open', 'in_progress', 'closed']:
            raise ValueError
        
        self._status = status
        
    @property
    def priority(self):
        return self._priority
    
    @priority.setter
    def priority(self, priority: str):
        if priority not in ['low', 'medium', 'high']:
            raise ValueError
        
        self._priority = priority
        
    def __str__(self):
        return f"Номер заявки: {self.id}\nНазвание: {self.title}\nСтатус: {self.status}\nПриоритет: {self.priority}"
    
    def to_dict(self) -> dict:
        data = {}
        data['id'] = self.id
        data['title'] = self.title
        data['status'] = self.status
        data['priority'] = self.priority
        if self.assigned_user:
            data['assigned_user'] = self.assigned_user.name 
        else:
            data['assigned_user'] = None
        return data
    
    @classmethod
    def from_dict(cls, data: dict):
        id = data['id']
        title = data['title']
        status = data['status']
        priority = data['priority']
        
        if data['assigned_user'] is not None:
            assigned_user = User(data['assigned_user'])
        else:
            assigned_user = None
        
        return cls(id, title, status, priority, assigned_user)
        
class TicketNotFoundError(KeyError):
    pass

class TicketTracker:
    def __init__(self):
        self.data: dict[int, Ticket] = {}
        self.ticket_id: int = 1
    
    def create_ticket(self, title: str, priority: str) -> None:
        self.data[self.ticket_id] = Ticket(self.ticket_id, title, "open", priority)
        self.ticket_id += 1
    
    def get_ticket(self, ticket_id: int) -> Ticket:
        if ticket_id in self.data:
            return self.data[ticket_id]
        raise TicketNotFoundError
    
    def assign_ticket(self, ticket_id: int, user: User) -> None:
        self.get_ticket(ticket_id).assigned_user = user

    def change_status(self, ticket_id: int, status: str) -> None:
        self.get_ticket(ticket_id).status = status
        
    def get_open_tickets(self) -> list[Ticket]:
        res = []
        for data in self.data.values():
            if data.status in ['open', 'in_progress']:
                res.append(data)
        return res
    
    def delete_ticket(self, ticket_id: int) -> None:
        self.get_ticket(ticket_id)
        del self.data[ticket_id]
    
    def save(self, filename: str) -> None:
        data = []
        for elem in self.data.values():
            data.append(elem.to_dict())
        
        with open(filename, 'w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
    @classmethod
    def load(cls, filename: str):
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
        
        tracker = cls()
        
        for elem in data:
            ticket = Ticket.from_dict(elem)
            tracker.data[ticket.id] = ticket
            
        max_id = (max(tracker.data.keys()) + 1) if tracker.data != {} else 1
        tracker.ticket_id = max_id
        
        return tracker
    
tracker = TicketTracker()
tracker.create_ticket("bish", "high")
tracker.create_ticket("bash", "low")
user = User("Alex")
tracker.assign_ticket(1, user)
tracker.change_status(1, "in_progress")
tracker.change_status(2, "closed")
tracker.save("tickets.json")
tracker2 = TicketTracker().load("tickets.json")
print(tracker2.get_open_tickets())
