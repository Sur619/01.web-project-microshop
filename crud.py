from typing import List

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from sqlalchemy.orm import joinedload, selectinload
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


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *posts_titles: str,
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    print("Posts created:", posts)
    return posts


async def get_users_posts(session: AsyncSession) -> List[Post]:
    stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)

    for user in users.unique():
        print("**" * 10)
        print(user)
        for post in user.posts:
            print(f"Post: {post.title}, Body: {post.body}")


async def get_posts_with_authors(session: AsyncSession) -> List[Post]:
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)
    for post in posts:
        print(f"Post: {post}, Author: {post.user}")


async def get_users_with_posts_and_profiles(session: AsyncSession) -> List[User]:
    stmt = (
        select(User)
        .options(joinedload(User.profile), selectinload(User.posts))
        .order_by(User.id)
    )
    users = await session.scalars(stmt)
    for user in users:
        print(f"User: {user.username}, Profile: {user.profile}, Posts: {user.posts}")


async def get_profile_with_users_and_users_with_posts(
    session: AsyncSession,
) -> List[Profile]:
    stmt = (
        select(Profile)
        .options(
            joinedload(Profile.user).selectinload(User.posts),
        )
        .order_by(Profile.id)
    )
    profiles = await session.scalars(stmt)
    for profile in profiles:
        print(profile.first_name, profile.user)
        print("Posts by user:", profile.user.posts)


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="john")
        # await create_user(session=session, username="ivan")
        user_john = await get_user_by_username(session=session, username="john")
        user_ivan = await get_user_by_username(session=session, username="ivan")
        #
        # await create_user_profile(
        #     session=session, user_id=user_ivan.id, first_name="ivan", last_name="bobby"
        # )
        # await create_user_profile(
        #     session=session, user_id=user_john.id, first_name="John", last_name="bobby"
        # )
        # await show_users_with_profiles(session=session)
        # await create_posts
        # await create_posts(session, user_john.id, "Math", "Physics", "Chemistry")
        # await get_users_posts(session=session)
        # await get_posts_with_authors(session=session)
        # await get_users_with_posts_and_profiles(session=session)
        await get_profile_with_users_and_users_with_posts(session=session)


if __name__ == "__main__":
    asyncio.run(main())
