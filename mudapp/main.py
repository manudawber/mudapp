from typing import List
from unicodedata import name
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from database import engine, get_session
from models import Base, TodoList, ListItem
from schemas import ListItemRequest, ListItemResponse, ListRequest, ListResponse

Base.metadata.create_all(engine)
app = FastAPI()


@app.get("/")
def read_root():
    """
    API information.
    """
    return {"message": "Mudapp to-do list, for all your shit."}


@app.get("/list", response_model=List[ListResponse])
def get_all_lists(session: Session = Depends(get_session)):
    """
    Return a list of all to-do lists stored by the app.
    """
    response = []
    lists = session.query(TodoList).all()
    for list in lists:
        items = session.query(ListItem).filter_by(id=list.id).all()
        list_response = ListResponse(
            id=list.id,
            name=list.name,
            items=[
                ListItemResponse(
                    id=item.id,
                    name=item.name,
                    completed=item.completed,
                    due_date=item.due_date if item.due_date else None,
                )
                for item in items
            ],
        )
        response.append(list_response)

    return response


@app.post("/list", response_model=ListResponse, status_code=status.HTTP_201_CREATED)
def create_list(request: ListRequest, session: Session = Depends(get_session)):
    """
    Create a to-do list using the request content.
    """
    # create list
    todo_list = TodoList(name=request.name)
    session.add(todo_list)
    session.commit()

    # create list items
    list_items = []
    if request.items:
        list_items = [
            ListItem(
                name=item.name,
                completed=False,
                due_date=item.due_date,
                id=todo_list.id
            ) for item in request.items
        ]
        session.add_all(list_items)
        session.commit()

    return ListResponse(id=todo_list.id, name=request.name, items=list_items)


@app.get("/list/{id}", response_model=ListResponse)
def get_list(id: int, session: Session = Depends(get_session)):
    """
    Return a specific list by ID.
    """
    list: TodoList = session.query(TodoList).get(id)
    if list is None:
        raise HTTPException(status_code=404, detail="List not found.")

    return ListResponse(id=list.id, name=list.name, items=list.items)


@app.put("/list/{id}", response_model=ListResponse)
def rename_list(
    id: int, request: ListRequest, session: Session = Depends(get_session)
):
    """
    Rename an existing to-do list.
    """
    list: TodoList = session.query(TodoList).get(id)
    if list is None:
        raise HTTPException(status_code=404, detail="List not found.")
    list.name = request.name
    session.commit()

    return ListResponse(id=list.id, name=list.name, items=list.items)


@app.delete("/list/{id}")
def delete_list(id: int, session: Session = Depends(get_session)):
    """
    Delete an existing to-do list.
    """
    list: TodoList = session.query(TodoList).get(id)
    if list is None:
        raise HTTPException(status_code=404, detail="List not found.")
    session.delete(list)
    session.commit()

    return {"message": "List deleted."}
