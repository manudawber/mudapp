from datetime import datetime
from lib2to3.pgen2.token import OP
from typing import List, Optional

from pydantic import BaseModel


class ListItemRequest(BaseModel):
    name: str
    due_date: Optional[datetime] = None


class ListItemResponse(BaseModel):
    id: str
    name: str
    completed: bool
    due_date: str


class ListRequest(BaseModel):
    name: str
    items: Optional[List[ListItemRequest]] = None


class ListResponse(ListRequest):
    id: str
    name: str
    items: List[ListItemResponse]
