import logging
from typing import List, Union

from fastapi import HTTPException

from app.models.pydantic import SummaryPayloadSchema
from app.models.tortoise import TextSummary
from app.summarizer import generate_summary

logging.basicConfig(filename="myapp.log", level=logging.INFO)


async def post(payload: SummaryPayloadSchema) -> int:
    article_summary = generate_summary(payload.url)
    logging.info(f"here is my article summary\n {article_summary}")
    summary = TextSummary(url=payload.url, summary=article_summary)
    await summary.save()
    return summary.id


async def get(id: int) -> Union[dict, None]:
    summary = await TextSummary.filter(id=id).first().values()
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


async def get_all() -> List:
    summaries = await TextSummary.all().values()
    return summaries


async def delete(id: int) -> int:
    summary = await TextSummary.filter(id=id).first().delete()
    return summary


async def put(id: int, payload: SummaryPayloadSchema) -> Union[dict, None]:
    summary = await TextSummary.filter(id=id).update(
        url=payload.url, summary=payload.summary
    )
    if summary:
        updated_summary = await TextSummary.filter(id=id).first().values()
        return updated_summary

    return None
