from aiogram.fsm.state import StatesGroup, State


class CommonStates(StatesGroup):
    awaiting_contact = State()


class GetOrdersStates(StatesGroup):
    SelectOrder = State()


class MakeOrderStates(StatesGroup):
    StartCity = State()
    EndCity = State()
    OrganizationName = State()
    LoadingAdress = State()
    Orientier = State()
    LoadingDateTime = State()
    DeliveryPackaging = State()
    DeliveryCount = State()
    TotalWeight = State()
    LoaderWorkerContact = State()
    DeliveryType = State()
    PaymentType = State()
    ValidateOrder = State()
    EditOrder = State()
    UpdateValue = State()