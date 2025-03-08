from sqlalchemy import create_engine
from models import *
from sqlalchemy.orm import sessionmaker


class DatabaseManager:
    def __init__(self, database_url):
        self.database_url = database_url
        self.engine = create_engine(self.database_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_or_update_user(self, user: User) -> User:
        db_user = self.session.query(User).filter_by(email=user.email).first()
        if db_user is None:
            db_user = user
        else:
            db_user.first_name = user.first_name
            db_user.second_name = user.second_name
            db_user.city = user.city
        self.session.add(db_user)
        self.session.commit()
        return db_user

    def create_or_update_item(self, item: Item) -> Item:
        db_item = self.session.query(Item).filter_by(name=item.name).first()
        if db_item is None:
            db_item = item
        else:
            db_item.price = item.price
            db_item.shops_n = item.shops_n
            db_item.rating = item.rating
            db_item.comments = item.comments
        self.session.add(db_item)
        self.session.commit()
        return db_item

    def create_item_user_relation(self, item: Item, user: User):
        if not item.id in [item.id for item in user.items]:
            user.items.append(item)
            self.session.add(user)
            self.session.commit()
