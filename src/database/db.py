from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

user = config.get('DB', 'USER')
passWOrd = config.get('DB', 'PASSWORD')
host = config.get('DB', 'HOST')
port = config.get('DB', 'PORT')
name = config.get('DB', 'NAME')

class Base(DeclarativeBase):
    pass

class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine = create_async_engine(url, echo=True)
        self._session_maker = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)

    async def session(self):
        async with self._session_maker() as session:
            yield session

url = f"postgresql+asyncpg://{user}:{passWOrd}@{host}:{port}/{name}"
sessionmanager = DatabaseSessionManager(url)
engine = create_async_engine(url)

async def get_db() -> AsyncSession:
    async for session in sessionmanager.session():
        yield session
