import json
import logging

import requests
import keyboards
from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import (Message, InlineKeyboardMarkup,
                           CallbackQuery,)
import states
from callback_datas import user_callback
from loader import dp

users= []
def init_photo_list():
    global users
    photos_markup = InlineKeyboardMarkup()
    btn_id = 0
    for user in users:
        photos_markup.add(
            types.InlineKeyboardButton(f'{user["author"]}  ({user["id"]})',
                                       callback_data=(f"post:{user['id']}:{btn_id}")),
        )
        btn_id += 1
    return photos_markup

@dp.message_handler(text="🔙 Back", state=states.Menu.JSON_Link)
async def get_back(message: types.Message):
    await states.Menu.Main_Menu.set()
    await message.answer('Main menu', reply_markup=keyboards.main_menu_markup)


@dp.callback_query_handler(text = 'back_to_list', state=states.PhotoList.Photo_Show)
async def return_photo_list(call: CallbackQuery):
    await call.message.answer_photo(photo="https://www.agroukr.ca/wp-content/uploads/2020/05/placeholder-img-3.jpg",
                               caption="Photo list", reply_markup=init_photo_list())
    await states.PhotoList.Show.set()
    await call.message.delete()


@dp.message_handler(CommandStart())
async def start(message: Message):
    text =  ("Hi, this is onboarding...\n"
             f"Send me a specific format link to a list of photos from picsum.photos like this:\n"
             f"https://picsum.photos/v2/list?page=2&limit=100")

    await message.answer(text)
    await states.Menu.JSON_Link.set()

@dp.message_handler(state=states.Menu.JSON_Link)
async def enter_link(message: types.Message):
    link = message.text
    try:
        response = requests.get(link)
        global users
        new_photos = json.loads(response.text)
        users.extend(new_photos)
    except Exception:
        await message.answer("wrong format or invalid link, try again")
    else:
        await message.answer("Photos saved")
        await states.Menu.Main_Menu.set()
        await message.answer('Main menu', reply_markup=keyboards.main_menu_markup)


@dp.message_handler(text="➕ Add new photos", state=states.Menu.Main_Menu)
async def add_photo(message: types.Message):
    await message.answer("Send me a specific format link to a list of photos from picsum.photos like this:\n"
             "https://picsum.photos/v2/list?page=2&limit=100", reply_markup=keyboards.text_back_markup)
    await states.Menu.JSON_Link.set()


@dp.message_handler(text="📃 Photo list", state=states.Menu.Main_Menu)
async def show_photo_list(message: types.Message):

    try:
        await message.answer_photo(photo="https://www.agroukr.ca/wp-content/uploads/2020/05/placeholder-img-3.jpg",
                                   caption="Photo list", reply_markup=init_photo_list())
        await message.answer(reply_markup=keyboards.main_menu_markup.ReplyKeyboardRemove())
    except Exception:
        await message.answer('Photo list', reply_markup=init_photo_list())
    await states.PhotoList.Show.set()


@dp.callback_query_handler(user_callback.filter(), state=states.PhotoList.Show)
async def show_chosen_photo(call: CallbackQuery):
    call_data = call.data.split(':')
    global current_user
    id = int(call_data[2])
    current_user = id
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    try:
        await call.message.answer_photo(photo=users[id]["url"], caption=f"Author: {users[id]['author']}\n"
                                                                    f"ID: {users[id]['id']}\n"
                                                                    f"Size: {users[id]['width']}x{users[id]['height']}\n"
                                                                    f"URL: {users[id]['url']}\n"
                                                                    f"Download URL: {users[id]['download_url']}", reply_markup=keyboards.post_markup)
        await call.message.delete()
        await states.PhotoList.Photo_Show.set()
    except Exception:
        await call.message.answer("Invalid photo, choose another one")


@dp.callback_query_handler(text = 'update_author', state=states.PhotoList.Photo_Show)
async def update_author(call: CallbackQuery):
    await call.message.answer('Enter a new author name', reply_markup=keyboards.line_back_markup)
    await states.PhotoList.Change_Author.set()


@dp.callback_query_handler(text = 'delete_photo', state=states.PhotoList.Photo_Show)
async def update_author(call: CallbackQuery):
    await call.message.answer('Are you sure you want to delete this photo?\n'
                              f'{users[current_user]["author"]} ({users[current_user]["id"]})', reply_markup=keyboards.accept_markup)
    await states.PhotoList.Delete_Photo.set()


@dp.callback_query_handler(text = 'back_to_photo', state=states.PhotoList.Change_Author)
async def return_photo(call: CallbackQuery):
    await call.message.delete()
    await states.PhotoList.Photo_Show.set()

@dp.callback_query_handler(text =('accept', 'decline'), state=states.PhotoList.Delete_Photo)
async def accepting_del(call: CallbackQuery):
    await call.message.delete()
    if call.data == 'accept':
        del users[current_user]
        await call.message.answer('The photo successfully deleted', reply_markup=keyboards.main_menu_markup)
        await states.Menu.Main_Menu.set()
    if call.data == 'decline':
        await states.PhotoList.Photo_Show.set()

@dp.message_handler(state=states.PhotoList.Change_Author)
async def show_photo_list(message: types.Message):
    try:
        new_author = message.text
        users[current_user]["author"] = new_author
        await message.answer('The author successfully updated')
        await states.Menu.Main_Menu.set()
        await message.answer('Main menu', reply_markup=keyboards.main_menu_markup)
    except Exception:
        await message.answer("Wrong name type, try again")


@dp.message_handler()
async def unknown_message(message: types.Message):
    await message.reply("Don't understand you, try again")