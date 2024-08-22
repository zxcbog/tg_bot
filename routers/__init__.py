__all__ = ("router",)

from aiogram import Router
from .admin_handlers import router as admin_router
from .common import router as common_router
from routers.callbacks import router as callback_router
from .order_handler import router as order_router

router = Router(name=__name__)

router.include_routers(
    admin_router,
    callback_router,
    order_router,
)

# this one has to be the last!
router.include_router(common_router)