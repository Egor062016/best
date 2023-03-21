from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
import telebot

import openai
import logging
import os

logging.basicConfig(level=logging.INFO)

bot1 = telebot.TeleBot('5619197827:AAERRo3fM1SwCE6l24DTTgpWwBNtFhFW8wM')

class PostState(StatesGroup):
    one = State()

class UserState(StatesGroup):
    one1 = State()

class ScamState(StatesGroup):
    onen = State()

banned_users = [5380685424 , 5272676030 , 731918546 , 1772411051 , 297820198 , 5710190212 , 5657609486 , 5828378741 , 5825904477 , 5380685424 , 5509031238]

storage = MemoryStorage()
bot = Bot('5619197827:AAERRo3fM1SwCE6l24DTTgpWwBNtFhFW8wM')
dp = Dispatcher(bot=bot,
                storage=storage)

os.environ(openai.api_key) = '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'

class Conversation(StatesGroup):
    waiting_for_input = State()

def sub():
    ikb = InlineKeyboardMarkup(row_width=1)
    item1 = InlineKeyboardButton(text='Биржа', url='https://t.me/YouTubeBirz')
    ikb.add(item1)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message_id)

    ikb = InlineKeyboardMarkup()

    item1 = InlineKeyboardButton(text='Я согласен✅', callback_data='agree')

    ikb.add(item1)
    await message.answer(f'<b>Я ознакомлен с <a href="https://telegra.ph/Pravila-ispolzovaniya-12-13">правилами использования</a> и соглашаюсь с ними</b>', parse_mode=ParseMode.HTML, reply_markup=ikb)


@dp.callback_query_handler(lambda c: c.data =='agree')
async def agree(call: types.CallbackQuery):
    await call.message.delete()

    ikb = InlineKeyboardMarkup()

    item1 = InlineKeyboardButton(text='Выложить пост📝', callback_data='post')
    item2 = InlineKeyboardButton(text='Профиль📱', callback_data='profile')
    item3 = InlineKeyboardButton(text='[БЕТА] ChatGPT🤖', callback_data='chat')
    item4 = InlineKeyboardButton(text='Сообщить о мошенничестве🚨', callback_data='scam')
    item5 = InlineKeyboardButton(text='Проверить пользователя👮🏻', callback_data='user')

    ikb.add(item1, item2)
    ikb.add(item3)
    ikb.add(item4, item5)
    await call.message.answer(f'<b>Добро пожаловать на автоматическую YouTube Биржу!</b>', reply_markup=ikb, parse_mode=ParseMode.HTML)

    await bot.answer_callback_query(call.id)

@dp.callback_query_handler(lambda c: c.data == 'chat')
async def post(call: types.CallbackQuery, state: FSMContext):
    user_channel_status = await bot.get_chat_member(chat_id='@YouTubeBirz', user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        if call.from_user.id in banned_users:
            await call.message.answer('Вы заблокированы⛔')
            return True
        else:
            ikb = InlineKeyboardMarkup(row_width=1)
            item1 = InlineKeyboardButton(text='Меню', callback_data='menu5')
            ikb.add(item1)

            await call.message.answer("Привет! Я бот на базе OpenAI GPT-3. Как я могу помочь тебе сегодня?", reply_markup=ikb)
            await Conversation.waiting_for_input.set()
            await bot.answer_callback_query(call.id)

            @dp.message_handler(state=Conversation.waiting_for_input)
            async def gpt_answer(message: types.Message, state: FSMContext):
                ikb = InlineKeyboardMarkup(row_width=1)
                item1 = InlineKeyboardButton(text='Меню', callback_data='menu6')
                ikb.add(item1)

                await message.answer("ChatGPT: Генерирую ответ ...")

                model_engine = "text-davinci-003"
                max_tokens = 128  # default 1024
                prompt = (message.text)
                completion = openai.Completion.create(
                    engine=model_engine,
                    prompt=prompt,
                    max_tokens=max_tokens,
                    temperature=0.5,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )

                translated_result = (completion.choices[0].text)
                await message.answer(translated_result, reply_markup=ikb)


    else:
        ikb = InlineKeyboardMarkup(row_width=1)
        item1 = InlineKeyboardButton(text='Биржа', url='https://t.me/YouTubeBirz')
        ikb.add(item1)

        await call.message.answer('Вы не подписаны на биржу!', reply_markup=ikb)

@dp.callback_query_handler(lambda c: c.data == 'menu6', state=Conversation.waiting_for_input)
async def menu5(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    ikb = InlineKeyboardMarkup()

    item1 = InlineKeyboardButton(text='Выложить пост📝', callback_data='post')
    item2 = InlineKeyboardButton(text='Профиль📱', callback_data='profile')
    item3 = InlineKeyboardButton(text='[БЕТА] ChatGPT🤖', callback_data='chat')
    item4 = InlineKeyboardButton(text='Сообщить о мошенничестве🚨', callback_data='scam')
    item5 = InlineKeyboardButton(text='Проверить пользователя👮🏻', callback_data='user')

    ikb.add(item1, item2)
    ikb.add(item3)
    ikb.add(item4, item5)
    await call.message.answer(f'<b>Добро пожаловать на автоматическую YouTube Биржу!</b>', reply_markup=ikb,
                              parse_mode=ParseMode.HTML)

    await bot.answer_callback_query(call.id)

@dp.callback_query_handler(lambda c: c.data == 'menu5', state=Conversation.waiting_for_input)
async def menu5(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(lambda c: c.data == 'post')
async def post(call: types.CallbackQuery):
    ikb = InlineKeyboardMarkup()

    item1 = InlineKeyboardButton(text='Меню', callback_data='menu')

    ikb.add(item1)

    user_channel_status = await bot.get_chat_member(chat_id='@YouTubeBirz', user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        if call.from_user.id in banned_users:
            await call.message.answer('Вы заблокированы⛔')
            return True
        else:
            await call.message.answer('Отправьте мне объявление\n<b>(Можно добавить до 1 фото/видео)</b>', reply_markup=ikb, parse_mode='HTML')
            await PostState.one.set()
    else:
        ikb = InlineKeyboardMarkup(row_width=1)
        item1 = InlineKeyboardButton(text='Биржа', url='https://t.me/YouTubeBirz')
        ikb.add(item1)

        await call.message.answer('Вы не подписаны на биржу!', reply_markup=ikb)

    await bot.answer_callback_query(call.id)

    @dp.message_handler(content_types=['text','photo'], state=PostState.one)
    async def ready(message: types.Message, state: FSMContext):
        ikb = InlineKeyboardMarkup()

        item1 = InlineKeyboardButton(text='Да', callback_data='yes')
        item2 = InlineKeyboardButton(text='Нет', callback_data='no')

        ikb.add(item1, item2)

        await message.answer(f'Объявление готово к публикации✅\n\n'
                             f'<b>Вы уверенны, что хотите опубликовать объявление?</b>', parse_mode=ParseMode.HTML,
                             reply_markup=ikb)

    @dp.message_handler(content_types=['text'], state=PostState.one)
    async def ready(message: types.Message, state: FSMContext):
        ikb = InlineKeyboardMarkup()

        item1 = InlineKeyboardButton(text='Да', callback_data='yes')
        item2 = InlineKeyboardButton(text='Нет', callback_data='no')

        ikb.add(item1, item2)

        await message.answer(f'Объявление готово к публикации✅\n\n'
                                f'<b>Вы уверенны, что хотите опубликовать объявление?</b>', parse_mode=ParseMode.HTML, reply_markup=ikb)

    @dp.message_handler(content_types=['text' ,'video'], state=PostState.one)
    async def ready(message: types.Message, state: FSMContext):
        ikb = InlineKeyboardMarkup()

        item1 = InlineKeyboardButton(text='Да', callback_data='yes')
        item2 = InlineKeyboardButton(text='Нет', callback_data='no')

        ikb.add(item1, item2)

        await message.answer(f'Объявление готово к публикации✅\n\n'
                             f'<b>Вы уверенны, что хотите опубликовать объявление?</b>', parse_mode=ParseMode.HTML,
                             reply_markup=ikb)

@dp.callback_query_handler(lambda c: c.data == 'yes', state=PostState.one)
async def yes(call: types.CallbackQuery, state: FSMContext):
    user_channel_status = await bot.get_chat_member(chat_id='@YouTubeBirz', user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        if call.from_user.id in banned_users:
            await call.message.answer('Вы заблокированы⛔')
            await state.finish()
            return True
        else:
            bot1.forward_message(-1001538332180, call.message.chat.id, call.message.message_id - 1)
            bot1.send_message(1807653203, f'Пост от @{call.from_user.username}')
            await call.message.answer('Объявление опубликовано✅')

            ikb = InlineKeyboardMarkup()

            item1 = InlineKeyboardButton(text='Выложить пост📝', callback_data='post')
            item2 = InlineKeyboardButton(text='Профиль📱', callback_data='profile')
            item3 = InlineKeyboardButton(text='[БЕТА] ChatGPT🤖', callback_data='chat')
            item4 = InlineKeyboardButton(text='Сообщить о мошенничестве🚨', callback_data='scam')
            item5 = InlineKeyboardButton(text='Проверить пользователя👮🏻', callback_data='user')

            ikb.add(item1, item2)
            ikb.add(item3)
            ikb.add(item4, item5)
            await call.message.answer(f'<b>Добро пожаловать на автоматическую YouTube Биржу!</b>', reply_markup=ikb,
                                      parse_mode=ParseMode.HTML)

            await state.finish()
    else:
        ikb = InlineKeyboardMarkup(row_width=1)
        item1 = InlineKeyboardButton(text='Биржа', url='https://t.me/YouTubeBirz')
        ikb.add(item1)
        await call.message.answer('Вы не подписаны на биржу!', reply_markup=ikb)

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
            await call.message.delete()
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
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-2)
            await state.finish()

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
                                      f'<b>Ник:</b> @{call.from_user.username}\n'
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

            item1 = InlineKeyboardButton(text='Выложить пост📝', callback_data='post')
            item2 = InlineKeyboardButton(text='Профиль📱', callback_data='profile')
            item3 = InlineKeyboardButton(text='[БЕТА] ChatGPT🤖', callback_data='chat')
            item4 = InlineKeyboardButton(text='Сообщить о мошенничестве🚨', callback_data='scam')
            item5 = InlineKeyboardButton(text='Проверить пользователя👮🏻', callback_data='user')

            ikb.add(item1, item2)
            ikb.add(item3)
            ikb.add(item4, item5)
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

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
