# Design

Basic to do list rest API backed by a sqlite DB.

```yaml
todo_list:
  id: 1
  name: MVP features
  owner: Manu
  items:
    - list_item:
        id: 1
        completed: false
        text: create list class
        due_date: 2022-11-1
    - list_item:
        id: 2
        completed: false
        text: create list_item class
        due_date: 2022-11-1
    - list_item:
        id: 3
        completed: false
        text: create request schemas
        due_date: 2022-11-1
    - list_item:
        id: 4
        completed: false
        text: create database models
        due_date: 2022-11-1
    - list_item:
        id: 5
        completed: false
        text: implement CRUD for lists
        due_date: 2022-11-1
    - list_item:
        id: 6
        completed: false
        text: implement CRUD for list_items
        due_date: 2022-11-1
```
