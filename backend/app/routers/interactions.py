"""Router for interaction endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.db.interactions import create_interaction, read_interactions
from app.models.interaction import (
    InteractionLog,
    InteractionLogCreate,
    InteractionModel,
)

router = APIRouter()


def filter_by_max_item_id(
    interactions: list[InteractionLog], max_item_id: int | None
) -> list[InteractionLog]:
    if max_item_id is None:
        return interactions
    return [i for i in interactions if i.item_id < max_item_id]


@router.get("/", response_model=list[InteractionModel])
async def get_interactions(
    max_item_id: int | None = None,
    session: AsyncSession = Depends(get_session),
):
    """Get all interactions, optionally filtered by maximum item ID."""
    interactions = await read_interactions(session)
    return filter_by_max_item_id(interactions, max_item_id)


@router.post("/", response_model=InteractionLog, status_code=201)
async def post_interaction(
    body: InteractionLogCreate, session: AsyncSession = Depends(get_session)
):
    """Create a new interaction log."""
    try:
        return await create_interaction(
            session,
            learner_id=body.learner_id,
            item_id=body.item_id,
            kind=body.kind,
        )
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc.orig),
        )
