from typing import List

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from sqlalchemy.orm import joinedload
from core.models import db_helper, User, Profile, Post


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    user: User | None = await session.scalar(stmt)
    print("User", user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name)
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession) -> List[User]:
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    # result: Result = await session.execute(stmt)
    # users = result.scalar()
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_name)


async def create_post(session: AsyncSession, user_id: int, *post_title: str, ) -> list[Post]:

async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="john")
        # await create_user(session=session, username="ivan")
        # user_john = await get_user_by_username(session=session, username="john")
        # user_ivan = await get_user_by_username(session=session, username="ivan")
        #
        # await create_user_profile(
        #     session=session, user_id=user_ivan.id, first_name="ivan", last_name="bobby"
        # )
        # await create_user_profile(
        #     session=session, user_id=user_john.id, first_name="John", last_name="bobby"
        # )
        await show_users_with_profiles(session=session)


if __name__ == "__main__":
    asyncio.run(main())
