from __future__ import annotations
from typing import Optional
from datetime import date

from ShipRatingslib.Domain import ReviewFramework
from ShipRatingslib.Domain.ReviewFramework import PreviousRating
from ShipRatingslib.Services import unit_of_work


class DuplicateReview(Exception):
    pass
    ShipName: str
    ShipID: str
    PriceofTicket: int
    QuantityOfTickets: int
    TicketId: int
    RatingNumber: float
    Text: str
    Problems: str


def add_batch(
    ShipName: str, ShipID: str, PriceofTicket: int, QuantityOfTickets: int, TicketId: int, RatingNumber: float,
    Text: str, Problems: str,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        Review = uow.Review.get(TicketId=TicketId)
        if Review is None:
            Review = ReviewFramework.PreviousRating(TicketId, batches=[])
            uow.Review.add(Review)
        Review.batches.append(ReviewFramework.Batch(TicketId, ShipName, ShipID, PriceofTicket,
                                                    QuantityOfTickets, TicketId, RatingNumber, Text, PriceofTicket, Problems))
        uow.commit()


def allocate(
    ShipName: str, ShipID: str, PriceofTicket: int, QuantityOfTickets: int, TicketId: int, RatingNumber: float,
    Text: str, Problems: str,
    uow: unit_of_work.AbstractUnitOfWork,
) -> str:
    line = PreviousRating(TicketId, ShipName, ShipID, PriceofTicket,
                          QuantityOfTickets, TicketId, RatingNumber, Text, Problems)
    with uow:
        Review = uow.Review.get(TicketId=line.TicketId)
        if Review is None:
            raise DuplicateReview(f"Duplicate Review {line.TicketId}")
        batchref = Review.allocate(line)
        uow.commit()
    return batchref
