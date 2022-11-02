from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class TodoList(Base):
    __tablename__ = "list"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    owner = Column(String(50))
    items = relationship("ListItem", backref="list")


class ListItem(Base):
    __tablename__ = "list_item"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    completed = Column(Boolean)
    due_date = Column(DateTime)
    list_id = Column(Integer, ForeignKey("list.id"))
