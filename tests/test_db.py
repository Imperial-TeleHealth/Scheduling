import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv(override=True)
DATABASE_URL = os.getenv('DATABASE_URL')


print(DATABASE_URL)

# find "40" in DATABASE_URL and replace it with %40

print(DATABASE_URL)


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_connection():
    try:
        # create a new session
        db = SessionLocal()
        
        # execute a simple query
        result = db.execute(text("SELECT 1"))
        
        # print the result
        print(result.fetchone())
        
        # close the session
        db.close()
        
        print("Connection successful")
    except Exception as e:
        print("Connection failed:", e)

test_connection()