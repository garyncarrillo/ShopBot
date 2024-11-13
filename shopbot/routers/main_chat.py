from fastapi import APIRouter, HTTPException
from .. import schemas

from ..services.main_chat_service import MainChatService

# Initialize the API router with the specified tag
router = APIRouter(
    tags = ['AI_Chat']
)

# Define a POST endpoint for handling main LLM chat requests
@router.post("/main-llm-chat")
def process_chat_request(
    chat_request: schemas.ChatSchema
):
    try:
        # Extract the initial query from the chat request
        query = chat_request.initial_query
        # Process the query through the main chat service and return the response
        return MainChatService().handlle_user_query(query=query)
    except Exception as e:
        # Raise an HTTP 422 error with details in case of any exceptions
        raise HTTPException(
            status_code=422,
            detail=f"main-ll-chat-endpoint: Chat {str(e)}"
        )