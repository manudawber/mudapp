from typing import List
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Response, status

from schemas import TodoListItemRequest, TodoListRequest, TodoListResponse

app = FastAPI()
list_collection = {
    "4bf691": TodoListRequest(
        name="Examples",
        items=[
            TodoListItemRequest(name="Make an example list"),
            TodoListItemRequest(name="Query the list using my API"),
        ],
    )
}


@app.get("/", response_model=List[TodoListResponse])
def read_root():
    """
    Return a list of all todo lists stored in the app.
    """
    return [
        TodoListResponse(id=id, **list.dict()) for id, list in list_collection.items()
    ]


@app.post("/list", response_model=TodoListResponse, status_code=status.HTTP_201_CREATED)
def create_list(request: TodoListRequest):
    """
    Create a todo list using the request content.
    """
    id = generate_id()
    list_collection[id] = request
    return TodoListResponse(id=id, **list_collection[id].dict())


@app.get("/list/{id}", response_model=TodoListResponse)
def read_list(id: str):
    """
    Get a list using the ID provided in the path.
    """
    try:
        return TodoListResponse(id=id, **list_collection[id].dict())
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")


@app.put("/list/{id}", response_model=TodoListResponse)
def update_list(id: str, request: TodoListRequest):
    if id not in list_collection:
        raise HTTPException(status_code=404, detail="Item not found")
    list_collection[id] = request
    return TodoListResponse(id=id, **list_collection[id].dict())


def generate_id():
    return uuid4().hex[:7]
