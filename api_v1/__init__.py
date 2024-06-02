from fastapi import APIRouter
from .products.views import router as products_router

router = APIRouter()
router.include_router(products_router)
