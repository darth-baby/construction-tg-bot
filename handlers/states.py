from aiogram.fsm.state import State, StatesGroup


class FeedbackStates(StatesGroup):
    WaitingForFeedback = State()  # Состояние ожидания сообщения
