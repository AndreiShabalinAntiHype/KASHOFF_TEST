from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship
from models.item_to_user import user_item_association
from models.base import Base


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    shops_n = Column(Integer, nullable=False)
    comments = relationship("Comment", back_populates="item")

    users = relationship(
        "User", secondary=user_item_association, back_populates="items"
    )
