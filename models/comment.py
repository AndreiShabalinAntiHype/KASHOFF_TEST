from models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    body = Column(String)

    item_id = Column(Integer, ForeignKey("items.id"))

    item = relationship("Item", back_populates="comments")
