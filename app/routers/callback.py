import httpx

from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import HttpUrl

# from ..dependencies import get_token_header
from ..models.invoice import Invoice, InvoiceEvent, InvoiceEventReceived

router = APIRouter(
    # prefix="/callback",
    tags=[
        "callback"
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

#-------------------
# OpenAPI callbacks

# The default path for receiving invoice event (the callback)

@router.post("/invoices/{invoice_id}")
def receive_invoice_event(invoice_id: str, event: InvoiceEvent):
    print({"id": invoice_id, "description": event.description, "paid": event.paid})

# The API with a path operation that could trigger a request to an external API

@router.post("{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived)
def invoice_notification(body: InvoiceEvent):
    pass

@router.post("/invoices/", callbacks=router.routes)
def create_invoice(
    invoice: Invoice, 
    background_tasks: BackgroundTasks, 
    callback_url: HttpUrl = "http://localhost:8000"
):
    """
    Create an invoice.

    This will let the API user (some external developer) create an invoice.

    And this path operation will:

    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification of the invoice event back to the API user, as a callback.
    
    """
    
    # Send the invoice, collect the money
    
    if callback_url:
        background_tasks.add_task(send_invoice_callback, str(callback_url), invoice.id)
        
    return {"msg": "Invoice received"}

# A real worker function to execute the callback asynchronously

async def send_invoice_callback(target_url: str, invoice_id: str):
    
    async with httpx.AsyncClient() as client:

        # Construct the payload matching the InvoiceEvent model
        payload = {"description": "payment_successful", "paid": True}
        
        # This mirrors the OpenAPI expression: {$callback_url}/invoices/{$request.body.id}
        templated_url = f"{target_url}invoices/{invoice_id}"
        
        # Make the actual HTTP request outwards to the external developer's API
        try:
            await client.post(templated_url, json=payload)
            
        except httpx.HTTPError as e:
            pass # Handle retry logic here
            print(e)
