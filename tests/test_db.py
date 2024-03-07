import asyncio
import os
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv(override=True)
DATABASE_URL = os.getenv('DATABASE_URL')

# create engine with pymssql
engine = create_async_engine('mssql+aioodbc://' + DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def test_connection():
    try:
        async with async_session() as session:
            async with session.begin():
                # Assuming User is your mapped class
                result = await session.execute(select(User).options(selectinload(User.roles)))
                user = result.scalars().first()
                print(user.name)  # Access the data in the user object

        print("Connection successful")
    except Exception as e:
        print("Connection failed:", e)

asyncio.run(test_connection())