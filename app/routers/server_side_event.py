from collections.abc import AsyncIterable, Iterable
from fastapi import APIRouter, Depends, Header
from fastapi.sse import EventSourceResponse, ServerSentEvent
from typing import Annotated

# from ..dependencies import get_token_header
from ..models.item import Item

router = APIRouter(
    prefix="/server-side-events",
    tags=[
        "server side event"
    ],
    dependencies=[
        # Depends(get_token_header)
    ],
    responses={
        404: {
            "description": "Not found"
        }
    },
)

items = [
    Item(name="Plumb",      description="A multi-purpose household device."),
    Item(name="Portal Gun", description="A portal opening device."),
    Item(name="Mee Box",    description="A box that summons a Mee."),
]

logs = [
    "2025-01-01 INFO  Application started",
    "2025-01-01 DEBUG Connected to database",
    "2025-01-01 WARN  High memory usage detected",
]
    
@router.get("/items/stream", response_class=EventSourceResponse)
async def stream_items() -> AsyncIterable[Item]: 
    for item in items:
        yield item

# If you need to set SSE fields like event, id, retry, or comment, you can yield 
# `ServerSentEvent` objects instead of plain data.

@router.get("/server-sent-events/stream", response_class=EventSourceResponse)
async def stream_server_sent_events() -> AsyncIterable[ServerSentEvent]:
    
    yield ServerSentEvent(comment="stream of item updates")
    
    for i, item in enumerate(items):
        yield ServerSentEvent(data=item, event="item_update", id=str(i + 1), retry=5000)

# When a browser reconnects after a connection drop, it sends the last received id 
# in the Last-Event-ID header.

# You can read it as a header parameter and use it to resume the stream from where 
# the client left off:
    
@router.get("/server-sent-events/stream-with-reconnect", response_class=EventSourceResponse)
async def stream_server_sent_events_with_reconnect(
    last_event_id: Annotated[int | None, Header()] = None,
) -> AsyncIterable[ServerSentEvent]:
    
    start = last_event_id + 1 if last_event_id is not None else 0
    
    for i, item in enumerate(items):
        if i < start:
            continue
        yield ServerSentEvent(data=item, id=str(i))

@router.get("/items/stream-no-async", response_class=EventSourceResponse)
def stream_items_no_async() -> Iterable[Item]:
    for item in items:
        yield item

# If you need to send data without JSON encoding, use raw_data instead of data.

@router.get("/logs/stream", response_class=EventSourceResponse)
async def stream_logs() -> AsyncIterable[ServerSentEvent]:
    for log_line in logs:
        yield ServerSentEvent(raw_data=log_line)
