__all__ = ("router",)

from aiogram import Router
from .order_callbacks import router as router_orders
from .common import router as router_com
from .channel_callbacks import router as router_channel

router = Router(name=__name__)

router.include_routers(
    router_com,
    router_orders,
    router_channel
)