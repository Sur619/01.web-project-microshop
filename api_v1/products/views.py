from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .dependencies import product_by_id
from . import crud
from core.models import db_helper
from .schemas import (
    Product,
    ProductCreate,
    ProductUpdate,
    ProductUpdatePartial,
)

router = APIRouter(tags=["Products"])


@router.get("/", response_model=list[Product])
async def get_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_products(session=session)


@router.get("/{product_id}/", response_model=Product | None)
async def get_product(
    product=Depends(product_by_id),
) -> Product | None:
    return product


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Product:
    return await crud.create_product(session=session, product_in=product_in)


@router.put("/{product_id}/", response_model=Product)
async def update_product(
    product_update: ProductUpdate,
    product=Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
    )


@router.patch("/{product_id}/", response_model=Product)
async def update_product_partial(
    product_update: ProductUpdatePartial,
    product=Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True,
    )


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product=Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_product(
        product=product,
        session=session,
    )
