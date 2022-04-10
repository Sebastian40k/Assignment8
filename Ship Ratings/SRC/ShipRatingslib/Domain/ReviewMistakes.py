from dataclasses import dataclass


class Event:
    pass


@dataclass
class DuplicateReview(Event):
    TicketId: str
