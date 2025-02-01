from sqlmodel import Session, SQLModel, create_engine, Session
from config import get_db_url

engine = create_engine(get_db_url())

def created_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session
        
def check_and_reconnect():
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except Exception as e:
        try:
            engine.dispose()
            with engine.connect() as connection:
                connection.execute("SELECT 1")
                return True
        except:
            return False