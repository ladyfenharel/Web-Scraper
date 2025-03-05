from sqlalchemy.orm import Session
from db import engine
import models
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def query_bookmarks(username: str):
    """Queries and displays bookmarks for a given username."""
    with Session(engine) as db:
        user = db.query(models.User).filter(models.User.username == username).first()

        if not user:
            logging.warning(f"User '{username}' not found.")
            print(f"User '{username}' not found.")
            return

        bookmarks = db.query(models.Bookmark).filter(models.Bookmark.user_id == user.id).all()

        if not bookmarks:
            logging.info(f"No bookmarks found for user '{username}'.")
            print(f"No bookmarks found for user '{username}'.")
            return

        for bookmark in bookmarks:
            print(f"Title: {bookmark.title}")
            print(f"Author: {bookmark.author}")
            print(f"Fandom: {bookmark.fandom}")
            print(f"Pairings: {bookmark.pairings}")
            print(f"Tags: {bookmark.tags}")
            print(f"Characters: {bookmark.characters}")
            print(f"Description: {bookmark.description}")
            print(f"Ratings: {bookmark.ratings}")
            print(f"Warnings: {bookmark.warnings}")
            print(f"Categories: {bookmark.categories}")
            print("-" * 20)

if __name__ == "__main__":
    username_to_query = input("Enter the username to query: ")
    query_bookmarks(username_to_query)