from sqlalchemy import Table, Column, Integer, ForeignKey
from models.base import Base

user_item_association = Table(
    "item_to_user",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("item_id", Integer, ForeignKey("items.id")),
)
