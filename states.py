from aiogram.dispatcher.filters.state import StatesGroup, State

class Menu(StatesGroup):
    JSON_Link = State()
    Main_Menu = State()

class PhotoList(StatesGroup):
    Show = State()
    Photo_Show = State()
    Change_Author = State()
    Delete_Photo = State()
