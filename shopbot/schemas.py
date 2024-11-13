from typing import Optional
from pydantic import BaseModel

class ChatSchema(BaseModel):
    initial_query: Optional[str] = None