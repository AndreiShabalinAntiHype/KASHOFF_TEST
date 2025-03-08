from models.base import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.item_to_user import user_item_association


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)

    email = Column(String)
    first_name = Column(String, nullable=True)
    second_name = Column(String, nullable=True)
    city = Column(String, nullable=True)

    items = relationship(
        "Item", secondary=user_item_association, back_populates="users"
    )
