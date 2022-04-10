from __future__ import annotations
from typing import TYPE_CHECKING
from ShipRatingslib.adapters import Email
from ShipRatingslib.Domain import ReviewCommands, ReviewMistakes, ReviewFramework
from ShipRatingslib.Domain.ReviewFramework import PreviousRating


if TYPE_CHECKING:
    from . import unit_of_work


class DuplicateReview(Exception):
    pass


def add_batch(
    cmd: ReviewCommands.CreateBatch,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        Review = uow.Review.get(TicketId=cmd.TicketId)
        if Review is None:
            Review = ReviewFramework.PreviousRating(cmd.TicketId, batches=[])
            uow.Review.add(Review)
        Review.batches.append(ReviewFramework.Batch(cmd.TicketId, cmd.ShipName, cmd.ShipID, cmd.PriceofTicket,
                                                    cmd.QuantityOfTickets, cmd.TicketId, cmd.RatingNumber, cmd.Text, cmd.PriceofTicket, cmd.Problems))
        uow.commit()


def allocate(
    cmd: ReviewCommands.Allocate,
    uow: unit_of_work.AbstractUnitOfWork,
) -> str:
    line = PreviousRating(cmd.TicketId, cmd.ShipName, cmd.ShipID, cmd.PriceofTicket,
                          cmd.QuantityOfTickets, cmd.TicketId, cmd.RatingNumber, cmd.Text, cmd.Problems)
    with uow:
        Review = uow.Review.get(TicketId=line.TicketId)
        if Review is None:
            raise DuplicateReview(f"Duplicate Review {line.TicketId}")
        batchref = Review.allocate(line)
        uow.commit()
    return batchref


def send_Duplicate_Review_notification(
    event: ReviewMistakes.DuplicateReview,
    uow: unit_of_work.AbstractUnitOfWork,
):
    Email.send(
        "stock@made.com",
        f"Duplicate Review {event.TicketId}",
    )
