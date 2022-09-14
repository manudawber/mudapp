from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class TodoListItemRequest(BaseModel):
    name: str
    description: Optional[str] = None


class TodoListRequest(BaseModel):
    name: str
    items: Optional[List[TodoListItemRequest]] = None


class TodoListResponse(TodoListRequest):
    id: str
