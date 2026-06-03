from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///./sports_events.db"

engine = create_engine(
    DATABASE_URL,
    echo=True, # useful for debugging, but should be set to False in production
    connect_args={"check_same_thread": False}  # Needed for SQLite to allow multiple threads
    )

def get_db():
    # This function is a generator that yields a database session. It is used as a dependency in the API endpoints to provide a session for database operations.
    with Session(engine) as session:
        yield session

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
