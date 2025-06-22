from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from sqlalchemy.orm import joinedload, selectinload
from core.models import (
    db_helper,
    User,
    Profile,
    Post,
    Order,
    Product,
    OrderProductAssociation,
)


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


async def create_order(
    session: AsyncSession,
    promocode: str | None = None,
) -> Order:
    order = Order(promocode=promocode)
    session.add(order)
    await session.commit()
    return order


async def create_product(
    session: AsyncSession,
    name: str,
    description: str,
    price: int,
):
    product = Product(
        name=name,
        description=description,
        price=price,
    )
    session.add(product)
    await session.commit()
    return product


async def main_relations(session: AsyncSession):
    await create_user(session=session, username="john")
    await create_user(session=session, username="ivan")
    user_john = await get_user_by_username(session=session, username="john")
    user_ivan = await get_user_by_username(session=session, username="ivan")

    await create_user_profile(
        session=session, user_id=user_ivan.id, first_name="ivan", last_name="bobby"
    )
    await create_user_profile(
        session=session, user_id=user_john.id, first_name="John", last_name="bobby"
    )
    await show_users_with_profiles(session=session)
    await create_posts(session, user_john.id, "Math", "Physics", "Chemistry")
    await get_users_posts(session=session)
    await get_posts_with_authors(session=session)
    await get_users_with_posts_and_profiles(session=session)
    await get_profile_with_users_and_users_with_posts(session=session)


async def create_orders_and_products(session: AsyncSession):
    order_one = await create_order(session=session)
    order_promo = await create_order(session=session, promocode="promo")

    mouse = await create_product(
        session=session, name="Mouse", description="Gaming Mouse", price=1000
    )
    keyboard = await create_product(
        session=session, name="keyboard", description="Gaming keyboard", price=3000
    )
    display = await create_product(
        session=session, name="display", description="Gaming display", price=5000
    )
    order_one = await session.scalar(
        select(Order)
        .where(Order.id == order_one.id)
        .options(
            selectinload(Order.products),
        ),
    )
    order_promo = await session.scalar(
        select(Order)
        .where(Order.id == order_promo.id)
        .options(
            selectinload(Order.products),
        ),
    )
    order_one.products.append(mouse)
    order_one.products.append(keyboard)
    order_promo.products.append(display)
    order_promo.products.append(mouse)
    order_promo.products.append(keyboard)
    await session.commit()


async def get_orders_with_products_assoc(session: AsyncSession) -> List[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            ),
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)
    return list(orders)


async def demo_get_orders_with_products_through_secondary(session: AsyncSession):
    # orders = await get_orders_with_products(session=session)
    # for order in orders:
    #     print(f"Order ID: {order.id}, Promocode: {order.promocode}")
    #     for product in order.products:
    #         print(f"  Product: {product.name}, Price: {product.price}")
    #
    ...


async def create_gift_product_for_existing_orders(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session)
    gift_product = await create_product(
        session=session, name="Gift", description="Gift Product", price=0
    )
    for order in orders:
        order.products_details.append(
            OrderProductAssociation(
                product=gift_product,
                count=1,
                unit_price=0,
            )
        )

    await session.commit()


async def demo_get_orders_with_products_with_assoc(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session=session)
    for order in orders:
        print(
            "id:",
            order.id,
            "promo:",
            order.promocode,
            "created:",
            order.created_at,
            "products:",
        )
        for order_product_details in order.products_details:
            print(
                "-",
                order_product_details.id,
                order_product_details.product.name,
                order_product_details.product.price,
                "qty:",
                order_product_details.count,
            )


async def demo_m2m(session: AsyncSession):
    # await demo_get_orders_with_products_through_secondary(session=session)
    # await create_gift_product_for_existing_orders(session=session)
    await demo_get_orders_with_products_with_assoc(session=session)


async def main():
    async with db_helper.session_factory() as session:
        await demo_m2m(session=session)


if __name__ == "__main__":
    asyncio.run(main())
