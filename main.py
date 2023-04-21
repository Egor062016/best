from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram.utils.markdown import hlink

import logging

import asyncio
from typing import List, Union

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

import telebot
import functions as func
import sqlite3
import time
from config import db

logging.basicConfig(level=logging.INFO)

bot1 = telebot.TeleBot('5619197827:AAF7Z6t-kb72ZQR8vH9nE03Xg0XkOxrUt7o')

class PostState(StatesGroup):
    one = State()

class UserState(StatesGroup):
    one1 = State()

class ScamState(StatesGroup):
    onen = State()

class SendState(StatesGroup):
    first = State()

banned_users = [5380685424 , 5272676030 , 731918546 , 1772411051 , 297820198 , 5710190212 , 5657609486 , 5828378741 , 5825904477 , 5380685424]

storage = MemoryStorage()
bot = Bot('5619197827:AAF7Z6t-kb72ZQR8vH9nE03Xg0XkOxrUt7o')
dp = Dispatcher(bot=bot,
                storage=storage)

bot_username = bot1.get_me().username

class Conversation(StatesGroup):
    waiting_for_input = State()

def sub():
    ikb = InlineKeyboardMarkup(row_width=1)
    item1 = InlineKeyboardButton(text='Биржа', url='https://t.me/YouTubeBirz')
    ikb.add(item1)


class AlbumMiddleware(BaseMiddleware):

    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        self.latency = latency
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        if not message.media_group_id:
            self.album_data[message.from_user.id] = [message]

            message.conf["is_last"] = True
            data["album"] = self.album_data[message.from_user.id]
            await asyncio.sleep(self.latency)
        else:
            try:
                self.album_data[message.media_group_id].append(message)
                raise CancelHandler()
            except KeyError:
                self.album_data[message.media_group_id] = [message]
                await asyncio.sleep(self.latency)

                message.conf["is_last"] = True
                data["album"] = self.album_data[message.media_group_id]

@dp.message_handler(commands=['admin'])
async def admin(message: types.Message, state: FSMContext):
    if message.from_user.id == 1807653203:
        ikb = InlineKeyboardMarkup(row_width=2)
        item1 = InlineKeyboardButton(callback_data='send', text='Рассылка')
        item2 = InlineKeyboardButton(callback_data='statistic', text='Статистика')
        ikb.add(item1, item2)

        await message.answer(f"{message.from_user.first_name}, вы авторизованы!", reply_markup=ikb)
    else:
        pass
        return

@dp.callback_query_handler(lambda c: c.data =='send')
async def sending(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id == 1807653203:
        await call.message.answer('Введите текст для рассылки. \n\nДля отмены напишите "-" без кавычек!')
        await SendState.first.set()
    else:
        pass
        return
    await bot.answer_callback_query(call.id)
    @dp.message_handler(content_types=['text'], state=SendState.first)
    async def reseption(message: types.Message):
        global text
        text = message.text

        ikb = InlineKeyboardMarkup(row_width=2)
        item1 = InlineKeyboardButton(callback_data='yes_send', text='Да')
        item2 = InlineKeyboardButton(callback_data='no_send', text='Нет')
        ikb.add(item1, item2)

        await message.answer(f'{call.from_user.first_name}, вы уверены, что хотите начать рассылку', reply_markup=ikb)

@dp.callback_query_handler(lambda c: c.data =='yes_send', state=SendState.first)
async def yes_menu(call: types.CallbackQuery, state: FSMContext):
    if call.message.text.startswith('-'):
        await call.message.answer('Отмена')
        await state.finish()
    else:
        info = admin_message(text)
        await call.message.answer('Рассылка начата!')
        for i in range(len(info)):
            try:
                time.sleep(1)
                await bot.send_message(admin_message(text)[i][0], str(text))
            except:
                pass
        await call.message.answer('Рассылка завершена!')
        await state.finish()
        print(info)
    await bot.answer_callback_query(call.id)

@dp.callback_query_handler(lambda c: c.data =='no_send', state=SendState.first)
async def no_menu(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Отмена')
    await state.finish()
    await bot.answer_callback_query(call.id)

@dp.callback_query_handler(lambda c: c.data =='statistic')
async def statistic(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(stats())
    await bot.answer_callback_query(call.id)


def admin_message(text):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(f'SELECT user_id FROM users')
    row = cursor.fetchall()
    return row
    conn.close()

def stats():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT user_id FROM users').fetchone()
    amount_user_all = 0
    while row is not None:
        amount_user_all += 1
        row = cursor.fetchone()
    msg = '❕ Информация:\n\n❕ Пользователей в боте - ' + str(amount_user_all)
    return msg
    conn.close()

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    chat_id = message.chat.id
    username = message.from_user.username

    func.first_join(user_id=chat_id, username=username)

    await bot.delete_message(message.from_user.id, message.message_id)

    ikb = InlineKeyboardMarkup()

    item1 = InlineKeyboardButton(text='Я согласен✅', callback_data='agree')

    ikb.add(item1)
    await message.answer(f'<b>Я ознакомлен с <a href="https://telegra.ph/Pravila-ispolzovaniya-12-13">правилами использования</a> и соглашаюсь с ними</b>', parse_mode=ParseMode.HTML, reply_markup=ikb)


@dp.callback_query_handler(lambda c: c.data =='agree')
async def agree(call: types.CallbackQuery):
    await call.message.delete()

    ikb = InlineKeyboardMarkup()

    item1 = InlineKeyboardButton(text='Выложить пост📝', callback_data='post1')
    item2 = InlineKeyboardButton(text='Профиль📱', callback_data='profile')
    item3 = InlineKeyboardButton(text='Сообщить о мошенничестве🚨', callback_data='scam')
    item4 = InlineKeyboardButton(text='Проверить пользователя👮🏻', callback_data='user')

    ikb.add(item1, item2)
    ikb.add(item3)
    ikb.add(item4)

    text=hlink('автоматическую YouTube Биржу', 'https://t.me/YouTubeBirz', disable_web_page_preview=False)

    await call.message.answer(f'<b>Добро пожаловать на text!</b>', reply_markup=ikb, parse_mode=ParseMode.HTML)

    await bot.answer_callback_query(call.id)

@dp.callback_query_handler(lambda c: c.data == 'menu6', state=Conversation.waiting_for_input)
async def menu5(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    ikb = InlineKeyboardMarkup()

    item1 = InlineKeyboardButton(text='Выложить пост📝', callback_data='post1')
    item2 = InlineKeyboardButton(text='Профиль📱', callback_data='profile')
    item3 = InlineKeyboardButton(text='Сообщить о мошенничестве🚨', callback_data='scam')
    item4 = InlineKeyboardButton(text='Проверить пользователя👮🏻', callback_data='user')

    ikb.add(item1, item2)
    ikb.add(item3)
    ikb.add(item4)
    await call.message.answer(f'<b>Добро пожаловать на автоматическую YouTube Биржу!</b>', reply_markup=ikb,
                              parse_mode=ParseMode.HTML)

    await bot.answer_callback_query(call.id)

@dp.callback_query_handler(lambda c: c.data == 'menu5', state=Conversation.waiting_for_input)
async def menu5(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(lambda c: c.data == 'post1')
async def post(call: types.CallbackQuery, state: FSMContext):
    ikb = InlineKeyboardMarkup()

    item1 = InlineKeyboardButton(text='Меню', callback_data='menu')

    ikb.add(item1)

    user_channel_status = await bot.get_chat_member(chat_id='@YouTubeBirz', user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        if call.from_user.id in banned_users:
            await call.message.answer('Вы заблокированы⛔')
            return True
        else:
            await call.message.answer('Отправьте мне объявление\n\n<b>Можно отправлять больше одного фото😎</b>', reply_markup=ikb, parse_mode='HTML')
    else:
        ikb = InlineKeyboardMarkup(row_width=1)
        item1 = InlineKeyboardButton(text='Биржа', url='https://t.me/YouTubeBirz')
        ikb.add(item1)

        await call.message.answer('Вы не подписаны на биржу!', reply_markup=ikb)

    @dp.message_handler(content_types=['text'])
    async def handle_albums(message: types.Message, state: FSMContext):
        user_channel_status = await bot.get_chat_member(chat_id='@YouTubeBirz', user_id=call.from_user.id)
        if user_channel_status["status"] != 'left':
            if call.from_user.id in banned_users:
                await call.message.answer('Вы заблокированы⛔')
                await state.finish()
                return True
            else:
                ikb = InlineKeyboardMarkup()

                item1 = InlineKeyboardButton(text='Да', callback_data='yes_text')
                item2 = InlineKeyboardButton(text='Нет', callback_data='no')

                ikb.add(item1, item2)

                await message.answer(f'Объявление готово к публикации✅\n\n'
                                     f'<b>Вы уверенны, что хотите опубликовать объявление?</b>',
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=ikb)
                await PostState.one.set()
        else:
            ikb = InlineKeyboardMarkup(row_width=1)
            item1 = InlineKeyboardButton(text='Биржа', url='https://t.me/YouTubeBirz')
            ikb.add(item1)
            await message.answer('Вы не подписаны на биржу!', reply_markup=ikb)

    await bot.answer_callback_query(call.id)


    @dp.message_handler(content_types=['text', 'photo'])
    async def handle_albums(message: types.Message, album: List[types.Message], state: FSMContext):
        user_channel_status = await bot.get_chat_member(chat_id='@YouTubeBirz', user_id=call.from_user.id)
        if user_channel_status["status"] != 'left':
            if call.from_user.id in banned_users:
                await call.message.answer('Вы заблокированы⛔')
                await state.finish()
                return True
            else:
                global media_group
                media_group = types.MediaGroup()
                for obj in album:
                    if obj.photo:
                        global file_id
                        file_id = obj.photo[-1].file_id
                        global caption
                        caption = album[0].caption
                    try:
                        media_group.attach({"media": file_id, "type": obj.content_type, 'chat_id': 1538332180})
                        media_group.media[0]["caption"] = caption
                    except ValueError:
                        return await message.answer("Ошибка. Напишите @EgorSelischev")

                ikb = InlineKeyboardMarkup()

                item1 = InlineKeyboardButton(text='Да', callback_data='yes')
                item2 = InlineKeyboardButton(text='Нет', callback_data='no')

                ikb.add(item1, item2)

                await message.answer(f'Объявление готово к публикации✅\n\n'
                                     f'<b>Вы уверенны, что хотите опубликовать объявление?</b>',
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=ikb)
                await PostState.one.set()
        else:
            ikb = InlineKeyboardMarkup(row_width=1)
            item1 = InlineKeyboardButton(text='Биржа', url='https://t.me/YouTubeBirz')
            ikb.add(item1)
            await message.answer('Вы не подписаны на биржу!', reply_markup=ikb)

    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(lambda c: c.data == 'yes_text', state=PostState.one)
async def yes(call: types.CallbackQuery, state: FSMContext):
    bot1.forward_message(-1001538332180, call.message.chat.id, call.message.message_id - 1)

    bot1.send_message(1807653203, f'Пост от @{call.from_user.username}')
    await call.message.answer('Объявление опубликовано✅')

    ikb = InlineKeyboardMarkup()

    item1 = InlineKeyboardButton(text='Выложить пост📝', callback_data='post1')
    item2 = InlineKeyboardButton(text='Профиль📱', callback_data='profile')
    item3 = InlineKeyboardButton(text='Сообщить о мошенничестве🚨', callback_data='scam')
    item4 = InlineKeyboardButton(text='Проверить пользователя👮🏻', callback_data='user')

    ikb.add(item1, item2)
    ikb.add(item3)
    ikb.add(item4)
    await call.message.answer(f'<b>Добро пожаловать на автоматическую YouTube Биржу!</b>',
                              reply_markup=ikb,
                              parse_mode=ParseMode.HTML)

    await state.finish()
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(lambda c: c.data == 'yes', state=PostState.one)
async def yes(call: types.CallbackQuery, state: FSMContext):
    await call.bot.send_media_group(chat_id=-1001538332180, media=media_group)

    bot1.send_message(1807653203, f'Пост от @{call.from_user.username}')
    await call.message.answer('Объявление опубликовано✅')

    ikb = InlineKeyboardMarkup()

    item1 = InlineKeyboardButton(text='Выложить пост📝', callback_data='post1')
    item2 = InlineKeyboardButton(text='Профиль📱', callback_data='profile')
    item3 = InlineKeyboardButton(text='Сообщить о мошенничестве🚨', callback_data='scam')
    item4 = InlineKeyboardButton(text='Проверить пользователя👮🏻', callback_data='user')

    ikb.add(item1, item2)
    ikb.add(item3)
    ikb.add(item4)
    await call.message.answer(f'<b>Добро пожаловать на автоматическую YouTube Биржу!</b>',
                         reply_markup=ikb,
                         parse_mode=ParseMode.HTML)

    await state.finish()
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(lambda c: c.data == 'menu', state=PostState.one)
async def yes(call: types.CallbackQuery, state: FSMContext):
    user_channel_status = await bot.get_chat_member(chat_id='@YouTubeBirz', user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        if call.from_user.id in banned_users:
            await call.message.answer('Вы заблокированы⛔')
            await state.finish()
            return True
        else:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            await state.finish()
    else:
        ikb = InlineKeyboardMarkup(row_width=1)
        item1 = InlineKeyboardButton(text='Биржа', url='https://t.me/YouTubeBirz')
        ikb.add(item1)
        await call.message.answer('Вы не подписаны на биржу!', reply_markup=ikb)

    await bot.answer_callback_query(call.id)

@dp.callback_query_handler(lambda c: c.data == 'no', state=PostState.one)
async def yes(call: types.CallbackQuery, state: FSMContext):
    user_channel_status = await bot.get_chat_member(chat_id='@YouTubeBirz', user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        if call.from_user.id in banned_users:
            await call.message.answer('Вы заблокированы⛔')
            await state.finish()
            return True
        else:
            await state.finish()

            ikb = InlineKeyboardMarkup()

            item1 = InlineKeyboardButton(text='Выложить пост📝', callback_data='post1')
            item2 = InlineKeyboardButton(text='Профиль📱', callback_data='profile')
            item3 = InlineKeyboardButton(text='Сообщить о мошенничестве🚨', callback_data='scam')
            item4 = InlineKeyboardButton(text='Проверить пользователя👮🏻', callback_data='user')

            ikb.add(item1, item2)
            ikb.add(item3)
            ikb.add(item4)
            await call.message.answer(f'<b>Добро пожаловать на автоматическую YouTube Биржу!</b>',
                                      reply_markup=ikb,
                                      parse_mode=ParseMode.HTML)
    else:
        ikb = InlineKeyboardMarkup(row_width=1)
        item1 = InlineKeyboardButton(text='Биржа', url='https://t.me/YouTubeBirz')
        ikb.add(item1)
        await call.message.answer('Вы не подписаны на биржу!', reply_markup=ikb)

    await bot.answer_callback_query(call.id)

@dp.callback_query_handler(lambda c: c.data == 'user')
async def user(call: types.CallbackQuery, state: FSMContext):
    user_channel_status = await bot.get_chat_member(chat_id='@YouTubeBirz', user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        if call.from_user.id in banned_users:
            await call.message.answer('Вы заблокированы⛔')
            return True
        else:
            await UserState.one1.set()
            ikb = InlineKeyboardMarkup()

            item1 = InlineKeyboardButton(text='Меню', callback_data='menu1')

            ikb.add(item1)

            await call.message.answer('Введите информацию о пользователе (Username, ID, карта, номер, киви кошелек и т.д.)', reply_markup=ikb)

            await bot.answer_callback_query(call.id)

            @dp.message_handler(state=UserState.one1)
            async def ready(message: types.Message, state: FSMContext):
                ikb1 = InlineKeyboardMarkup()

                item1 = InlineKeyboardButton(text='Меню', callback_data='menu2')

                ikb1.add(item1)

                word = message.text

                dicfile = open("base.txt", encoding="utf8")
                file1 = dicfile.read()

                if word in file1:
                    await message.answer(f'<b>Пользователь найден в базе✅</b>\n\n'
                                                      'Не советую проводить сделки с данным человеком', parse_mode=ParseMode.HTML,
                                     reply_markup=ikb1)
                else:
                    await message.answer(f'<b>Пользователь НЕ найден в базе❌</b>', parse_mode=ParseMode.HTML,
                                     reply_markup=ikb1)
                await state.finish()

    else:
        ikb = InlineKeyboardMarkup(row_width=1)
        item1 = InlineKeyboardButton(text='Биржа', url='https://t.me/YouTubeBirz')
        ikb.add(item1)
        await call.message.answer('Вы не подписаны на биржу!', reply_markup=ikb)

    await bot.answer_callback_query(call.id)

@dp.callback_query_handler(lambda c: c.data == 'menu1', state=UserState.one1)
async def menu1(call: types.CallbackQuery, state: FSMContext):
    user_channel_status = await bot.get_chat_member(chat_id='@YouTubeBirz', user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        if call.from_user.id in banned_users:
            await call.message.answer('Вы заблокированы⛔')
            await state.finish()
            return True
        else:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            await state.finish()

            await bot.answer_callback_query(call.id)

    else:
        ikb = InlineKeyboardMarkup(row_width=1)
        item1 = InlineKeyboardButton(text='Биржа', url='https://t.me/YouTubeBirz')
        ikb.add(item1)
        await call.message.answer('Вы не подписаны на биржу!', reply_markup=ikb)

    await bot.answer_callback_query(call.id)

@dp.callback_query_handler(lambda c: c.data == 'menu2')
async def menu2(call: types.CallbackQuery):
    user_channel_status = await bot.get_chat_member(chat_id='@YouTubeBirz', user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        if call.from_user.id in banned_users:
            await call.message.answer('Вы заблокированы⛔')
            return True
        else:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 2)

            await bot.answer_callback_query(call.id)

    else:
        ikb = InlineKeyboardMarkup(row_width=1)
        item1 = InlineKeyboardButton(text='Биржа', url='https://t.me/YouTubeBirz')
        ikb.add(item1)
        await call.message.answer('Вы не подписаны на биржу!', reply_markup=ikb)

    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(lambda c: c.data == 'profile')
async def menu3(call: types.CallbackQuery):
    user_channel_status = await bot.get_chat_member(chat_id='@YouTubeBirz', user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        if call.from_user.id in banned_users:
            await call.message.answer('Вы заблокированы⛔')
            return True
        else:
            ikb = InlineKeyboardMarkup()

            item1 = InlineKeyboardButton(text='Меню', callback_data='menu3')

            ikb.add(item1)

            await call.message.answer(f'<b>Имя:</b> {call.from_user.first_name}\n'
                                      f'<b>Username:</b> @{call.from_user.username}\n'
                                      f'<b>ID:</b> {call.from_user.id}', parse_mode=ParseMode.HTML, reply_markup=ikb)

            await bot.answer_callback_query(call.id)

    else:
        ikb = InlineKeyboardMarkup(row_width=1)
        item1 = InlineKeyboardButton(text='Биржа', url='https://t.me/YouTubeBirz')
        ikb.add(item1)
        await call.message.answer('Вы не подписаны на биржу!', reply_markup=ikb)

    await bot.answer_callback_query(call.id)

@dp.callback_query_handler(lambda c: c.data == 'menu3')
async def menu3(call: types.CallbackQuery):
    user_channel_status = await bot.get_chat_member(chat_id='@YouTubeBirz', user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        if call.from_user.id in banned_users:
            await call.message.answer('Вы заблокированы⛔')
            return True
        else:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            await bot.answer_callback_query(call.id)
    else:
        ikb = InlineKeyboardMarkup(row_width=1)
        item1 = InlineKeyboardButton(text='Биржа', url='https://t.me/YouTubeBirz')
        ikb.add(item1)
        await call.message.answer('Вы не подписаны на биржу!', reply_markup=ikb)

    await bot.answer_callback_query(call.id)

@dp.callback_query_handler(lambda c: c.data == 'scam')
async def yes(call: types.CallbackQuery, state: FSMContext):
    user_channel_status = await bot.get_chat_member(chat_id='@YouTubeBirz', user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        if call.from_user.id in banned_users:
            await call.message.answer('Вы заблокированы⛔')
            return True
        else:
            ikb = InlineKeyboardMarkup()

            item1 = InlineKeyboardButton(text='Меню', callback_data='menu4')

            ikb.add(item1)

            await call.message.answer('Предоставьте свой ник, ник мошенника, доказательства обмана, а также любую другую информацию о мошеннике.\n'
                                      'Можно отправлять больше, чем 1 сообщение' ,reply_markup=ikb)

            await ScamState.onen.set()

            await bot.answer_callback_query(call.id)

            @dp.message_handler(content_types=['text'], state=ScamState.onen)
            async def scaam (message: types.Message, state: FSMContext):
                ikb = InlineKeyboardMarkup()

                item1 = InlineKeyboardButton(text='Закрыть', callback_data='close')

                ikb.add(item1)

                bot1.forward_message(1807653203, call.message.chat.id, message.message_id)

                await message.answer('Отправил!', reply_markup=ikb)

            @dp.message_handler(content_types=['text', 'photo'], state=ScamState.onen)
            async def scaam(message: types.Message, state: FSMContext):
                ikb = InlineKeyboardMarkup()

                item1 = InlineKeyboardButton(text='Закрыть', callback_data='close')

                ikb.add(item1)

                bot1.forward_message(1807653203, call.message.chat.id, message.message_id)

                await message.answer('Отправил!', reply_markup=ikb)

            @dp.message_handler(content_types=['text', 'video'], state=ScamState.onen)
            async def scaam(message: types.Message, state: FSMContext):
                ikb = InlineKeyboardMarkup()

                item1 = InlineKeyboardButton(text='Закрыть', callback_data='close')

                ikb.add(item1)

                bot1.forward_message(1807653203, call.message.chat.id, message.message_id)

                await message.answer('Отправил!', reply_markup=ikb)

    else:
        ikb = InlineKeyboardMarkup(row_width=1)
        item1 = InlineKeyboardButton(text='Биржа', url='https://t.me/YouTubeBirz')
        ikb.add(item1)
        await call.message.answer('Вы не подписаны на биржу!', reply_markup=ikb)

    await bot.answer_callback_query(call.id)

@dp.callback_query_handler(lambda c: c.data == 'close', state=ScamState.onen)
async def close(call: types.CallbackQuery, state: FSMContext):
    user_channel_status = await bot.get_chat_member(chat_id='@YouTubeBirz', user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        if call.from_user.id in banned_users:
            await call.message.answer('Вы заблокированы⛔')
            await state.finish()
            return True
        else:
            await call.message.answer('Закрыто!')
            bot1.send_message(1807653203, f'Жалоба от @{call.from_user.username}')

            ikb = InlineKeyboardMarkup()

            item1 = InlineKeyboardButton(text='Выложить пост📝', callback_data='post1')
            item2 = InlineKeyboardButton(text='Профиль📱', callback_data='profile')
            item3 = InlineKeyboardButton(text='Сообщить о мошенничестве🚨', callback_data='scam')
            item4 = InlineKeyboardButton(text='Проверить пользователя👮🏻', callback_data='user')

            ikb.add(item1, item2)
            ikb.add(item3)
            ikb.add(item4)
            await call.message.answer(f'<b>Добро пожаловать на автоматическую YouTube Биржу!</b>', reply_markup=ikb,
                                      parse_mode=ParseMode.HTML)

            await state.finish()
    else:
        ikb = InlineKeyboardMarkup(row_width=1)
        item1 = InlineKeyboardButton(text='Биржа', url='https://t.me/YouTubeBirz')
        ikb.add(item1)
        await call.message.answer('Вы не подписаны на биржу!', reply_markup=ikb)

    await bot.answer_callback_query(call.id)

@dp.callback_query_handler(lambda c: c.data == 'menu4', state=ScamState.onen)
async def close(call: types.CallbackQuery, state: FSMContext):
    user_channel_status = await bot.get_chat_member(chat_id='@YouTubeBirz', user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        if call.from_user.id in banned_users:
            await call.message.answer('Вы заблокированы⛔')
            await state.finish()
            return True
        else:
            await call.message.delete()
            await state.finish()
    else:
        ikb = InlineKeyboardMarkup(row_width=1)
        item1 = InlineKeyboardButton(text='Биржа', url='https://t.me/YouTubeBirz')
        ikb.add(item1)
        await call.message.answer('Вы не подписаны на биржу!', reply_markup=ikb)

    await bot.answer_callback_query(call.id)

if __name__ == "__main__":
    dp.middleware.setup(AlbumMiddleware())
    executor.start_polling(dp, skip_updates=True)
