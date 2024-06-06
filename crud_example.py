import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload, selectinload

from core.db_helper import db_helper
from core.models import User, Post, Profile, Order, Product, OrderProductAssociation


# ВСЕ ЧТО НЕ m2m Связь
# добавление пользователя
async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


# получить юзера по юзернейму
async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # user: User | None = result.scalar_one_or_none()
    user: User | None = await session.scalar(stmt)
    print("found user", username, user)
    return user


# Создаем профиль для юзера
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


# Показываем юзеров и их профили
async def show_users_with_profiles(session: AsyncSession):
    stmt = (
        select(User).options(joinedload(User.profile)).order_by(User.id)
    )  # joinedload - просим подгрузить вместе с пользователями их профили (соединяеим 2 запроса)
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_name)


# создаем посты для юзера
async def create_post(
    session: AsyncSession,
    user_id: int,
    *post_titles: str,
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in post_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


# показываем юзеров и их посты
async def get_users_with_posts(session: AsyncSession):
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    stmt = (
        select(User)
        .options(
            # joinedload(User.posts)
            selectinload(
                User.posts
            )  # подгружает посты отдельно и пользователи не будут повторно загружены
        )
        .order_by(User.id)
    )
    result: Result = await session.execute(stmt)
    users = result.scalars()
    # users = await session.scalars(stmt)
    for user in users:
        print("**" * 10)
        print(user)
        for post in user.posts:
            print("--", post)


# запрашиваем посты и их авторов
async def get_posts_with_author(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)
    for post in posts:
        print("post", post)
        print("author", post.user, "\n")


# Запрашиваем юзеров с их постами и профилями
async def get_users_with_posts_and_profiles(session: AsyncSession):
    stmt = (
        select(User)
        .options(
            joinedload(User.profile),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    users = await session.scalars(stmt)
    for user in users:
        print("**" * 10)
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print("--", post)


# запрашиваем профили с юзером и их постами
async def get_profiles_with_user_and_posts(
    session: AsyncSession,
):
    stmt = (
        select(Profile)
        .options(joinedload(Profile.user).selectinload(User.posts))
        .order_by(Profile.id)
    )
    profiles = await session.scalars(stmt)
    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts, "\n")


async def get_profiles_with_user_and_posts_with_filter_by_user(
    session: AsyncSession, username: str
):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(joinedload(Profile.user).selectinload(User.posts))
        .where(User.username == username)
        .order_by(Profile.id)
    )
    profiles = await session.scalars(stmt)
    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts, "\n")


async def main_relations(session: AsyncSession):
    # СОЗДАНИЕ ПОЛЬЗОВАТЕЛЕЙ:
    # await create_user(session=session, username="john")
    # await create_user(session=session, username="nick")
    # await create_user(session=session, username="alice")

    # ИЩЕМ ПОЛЬЗОВАТЕЛЕЙ ПО ЮЗЕРНЕЙМУ
    # user_nick = await get_user_by_username(session=session, username="nick")
    # user_john = await get_user_by_username(session=session, username="john")
    # user_alice = await get_user_by_username(session=session, username="alice")

    # СОЗДАЕМ ПРОФИЛИ ДЛЯ ПОЛЬЗОВАТЕЛЕЙ
    # await create_user_profile(
    #     session=session, user_id=user_john.id, first_name="John"
    # )
    # await create_user_profile(
    #     session=session, user_id=user_nick.id, first_name="nick", last_name="White"
    # )

    # показываем всех пользователей с их профилями
    # await show_users_with_profiles(session=session)

    # создаем посты
    # await create_post(session, user_john.id, "Первый пост", "Второй пост")
    # await create_post(session, user_nick.id, "Fast API", "FAST API MORE")

    # запрашиваем пользователей с их постами:
    # await get_users_with_posts(session=session)

    # запрашиваем посты и их авторов
    # await get_posts_with_author(session=session)

    # запрашиваем юзеров с постами и профилями
    # await get_users_with_posts_and_profiles(session=session)

    # запрашиваем профили с их юзерами и их постами
    # await get_profiles_with_user_and_posts(session=session)

    await get_profiles_with_user_and_posts_with_filter_by_user(
        session=session, username="john"
    )


# m2m:
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
) -> Product:
    product = Product(
        name=name,
        description=description,
        price=price,
    )
    session.add(product)
    await session.commit()
    return product


async def create_orders_and_products(session: AsyncSession):
    order_one = await create_order(session)
    order_promo = await create_order(session, promocode="promo")

    mouse = await create_product(
        session,
        "Mouse",
        "Great gaming mouse",
        price=123,
    )
    keyboard = await create_product(
        session,
        "Keyboard",
        "Great gaming keyboard",
        price=149,
    )
    display = await create_product(
        session,
        "Display",
        "Office display",
        price=299,
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
    order_promo.products.append(keyboard)
    order_promo.products.append(display)

    order_promo.products = [keyboard, display]
    mouse_two = await create_product(
        session,
        "Mouse_Two",
        "Great gaming mouse_two",
        price=2534,
    )
    order_one.products.append(mouse_two)
    await session.commit()


async def get_orders_with_products(session: AsyncSession) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products),
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)

    return list(orders)


async def demo_get_orders_with_products_through_secondary(session: AsyncSession):
    orders = await get_orders_with_products(session)
    for order in orders:
        print(order.id, order.promocode, order.created_at, "products:")
        for product in order.products:  # type: Product
            print("-", product.id, product.name, product.price)


async def get_orders_with_products_assoc(session: AsyncSession) -> list[Order]:
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


async def demo_get_orders_with_products_with_assoc(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session)

    for order in orders:
        print(order.id, order.promocode, order.created_at, "products:")
        for (
            order_product_details
        ) in order.products_details:  # type: OrderProductAssociation
            print(
                "-",
                order_product_details.product.id,
                order_product_details.product.name,
                order_product_details.product.price,
                "qty:",
                order_product_details.count,
            )


async def create_gift_product_for_existing_orders(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session)
    gift_product = await create_product(
        session,
        name="Gift",
        description="Gift for you",
        price=0,
    )
    for order in orders:
        order.products_details.append(
            OrderProductAssociation(
                count=1,
                unit_price=0,
                product=gift_product,
            )
        )

    await session.commit()


async def demo_m2m(session: AsyncSession):
    # await create_orders_and_products(session)
    await demo_get_orders_with_products_through_secondary(session)
    await demo_get_orders_with_products_with_assoc(session)
    # await create_gift_product_for_existing_orders(session)


async def main():
    async with db_helper.section_factory() as session:
        # await main_relations(session)
        await demo_m2m(session)


if __name__ == "__main__":
    asyncio.run(main())
