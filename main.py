from config import *
from dotenv import load_dotenv
from database import DatabaseManager
from scrapper import Scrapper


def main():
    load_dotenv(".env.example")
    db = DatabaseManager(f"sqlite:///{get_db_url()}")
    parser = Scrapper(database=db)
    user = parser.parse_user(email=get_email(), password=get_password())
    parser.fill_items_list(user=user)


if __name__ == "__main__":
    main()
