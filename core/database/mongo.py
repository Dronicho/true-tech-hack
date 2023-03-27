import motor.motor_asyncio

MONGO_DETAILS = "mongodb://root:example@127.0.0.1:27017/"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.videos

async def get_mongo_session():
    """
    Get the database session.
    This can be used for dependency injection.

    :return: The database session.
    """
    try:
        yield database
    finally:
        print('susa')
