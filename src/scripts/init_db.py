from db.connection import engine, get_session
from db.initialise import initialise_database

if __name__ == "__main__":
    with get_session() as session:
        initialise_database(engine, session)
