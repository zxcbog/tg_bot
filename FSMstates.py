from aiogram.fsm.state import StatesGroup, State


class CommonStates(StatesGroup):
    awaiting_contact = State()


class DataCheckStates(StatesGroup):
    DataCheck = State()


class GetOrdersStates(StatesGroup):
    SelectOrder = State()
    OrderSelected = State()


class MakeOrderStates(StatesGroup):
    StartCity = State()
    Warehouse = State()
    EndCity = State()
    OrganizationName = State()
    LoadingAdress = State()
    Orientier = State()
    LoadingDateTime = State()
    DeliveryDateTime = State()
    DeliveryPackaging = State()
    DeliveryCount = State()
    TotalWeight = State()
    LoaderWorkerContact = State()
    DeliveryType = State()
    PaymentType = State()
    ValidateOrder = State()
    EditOrder = State()
    UpdateValue = State()