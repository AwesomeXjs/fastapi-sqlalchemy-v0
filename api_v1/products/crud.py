# create read update delete
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product
from .schemas import ProductCreate, ProductUpdate, ProductUpdatePartial


# внутрь функций нужно передавать сессию чтобы запрашивать какие то данные
async def get_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_one_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(
    session: AsyncSession, product_create: ProductCreate
) -> Product:
    product = Product(**product_create.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


# put - обновляет целиком, patch - обновляет некоторые поля
async def update_products(
    session: AsyncSession,
    product: Product,
    product_update: ProductUpdate | ProductUpdatePartial,
    partial: bool = False,
) -> Product:
    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)
    await session.commit()
    return product


async def delete_product(session: AsyncSession, product: Product):
    await session.delete(product)
    await session.commit()
