from libgravatar import Gravatar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.model import User
from src.schemas import UserSchema,UserResponseSchema


async def get_user_by_email(email: str, db: AsyncSession) -> User:
    sq = select(User).filter(User.email == email)
    result = await db.execute(sq)
    user = result.scalar()
    return user

async def user_to_response_schema(user: User) -> UserResponseSchema:
    return UserResponseSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        avatar=user.avatar
    )

async def create_user(body: UserSchema, db: AsyncSession) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    user_data = body.dict()
    new_user = User(**user_data, avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession) -> None:
    user.refresh_token = token
    await db.commit()

async def confirmed_email(email: str, db: AsyncSession) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()

async def update_avatar(email, url: str, db: AsyncSession) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    return user