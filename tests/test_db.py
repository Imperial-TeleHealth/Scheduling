# import asyncio
# import os
# from sqlalchemy import text
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv


# load_dotenv(override=True)
# DATABASE_URL = os.getenv('DATABASE_URL')

# # create engine with pymssql
# engine = create_async_engine('mssql+aioodbc://' + DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# # Create an asynchronous session factory
# # async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# from sqlalchemy import text

# async def test_connection():
#     try:
#         async with SessionLocal() as session:
#             async with session.begin():
#                 result = await session.execute(text("SELECT 1"))
#                 value = result.scalar_one()
#                 print(value)  # Should print 1

#         print("Connection successful")
#     except Exception as e:
#         print("Connection failed:", e)
#     finally:
#         await engine.dispose()

# asyncio.run(test_connection())
