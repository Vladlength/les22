from aiogram.utils import executor
import asyncio
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram import Bot, types

import config
import keyboard
import logging

storage = MemoryStorage()
bot = Bot(token=config.botkey, parse_mode=types.ParseMode.HTML)  # инициализируем бота
dp = Dispatcher(bot, storage=storage)  # инициализируем диспатчер к нащему боту

logging.basicConfig(filename='log.txt',
                    format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO
                    )  # включаем логирование


async def on_startup_(_):
    print(('бот запущен'))


# handler будет обрабатывать какие-либо обновления
@dp.message_handler(Command('start'), state=None)  # указываем боту на какую команду надо реагировать
async def welcome(message):
    with open("user.txt", "r") as JoinedFile:
        # создаем множество из ид пользователей
        JoinedUsers = set()
        for line in JoinedFile:
            JoinedUsers.add(line.strip())

    if not str(message.chat.id) in JoinedUsers:  # если в множестве нет ид этого пользователя
        # дописываем его в файл и в множество
        with open("user.txt", "a") as JoinedFile:
            JoinedFile.write(str(message.chat.id) + '\n')
            JoinedUsers.add(message.chat.id)

    await bot.send_message(message.chat.id, f"ПРИВЕТ, *{message.from_user.first_name}, *БОТ РАБОТАЕТ",
                           reply_markup=keyboard.start, parse_mode="Markdown")
    # бот отсылает сообщение с текстом и выводит клавиатуру start
    await bot.send_sticker(message.chat.id,
                           sticker='CAACAgIAAxkBAAEI75pkW9RZTlpLamK2Ul6z-9-J3kqwvAACRwEAAntOKhAtvk07cY4gsC8E')
    # бот отправляет стикер (с указанным ID) в чат message.chat.id. ID стикера - Get Sticker ID


@dp.message_handler(content_types=['text'])  # content_types = ['sticker'] если присылают стикер
async def get_message(message: types.Message):
    if message.text == 'Информация':
        await bot.send_message(message.chat.id, text='🧐' + '*Информация*\nБот создан специально для обучения',
                               parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())  # эмодзи можно скопировать в тг и просто текстом вставить
        # reply_markup = ReplyKeyboardRemove() уберет клавиатуру
# await message.delete()
# await message.reply(text='*Информация*\nБот создан специально для обучения',
#                        parse_mode='Markdown')
# await message.answer(text='*Информация*\nБот создан специально для обучения',
#                        parse_mode='Markdown')

# bot.send_message бот отправляет сообщение
# message.answer бот отправляет сообщение
# message.reply бот отвечает на сообщение
# message.delete() удалит отправленное сообщение


# для реализации методов message нужно указать types.Message

@dp.message_handler(content_types=['sticker'])
async def get_message_id(message: types.Message):
    await message.reply(message.sticker.file_id)
    # если пришел стикер отвечает текстом с ид этого стикера


@dp.message_handler(content_types=['text'])
async def echo(message: types.Message):
    await message.answer(message.text)  # эквивалентны
    await bot.send_message(chat_id=message.from_user.id,
                           text='HY')  # эквивалентны. Будут отправлять сообщения пользователю написавшему сообщение
    await bot.send_message(chat_id=message.chat.id,
                           text='HY')  # будет отправлять сообщение в тот чат в котором написано сооощение
    await bot.send_photo(chat_id=message.from_user.id,
                         photo="https://static-cse.canva.com/blob/847132/paulskorupskas7KLaxLbSXAunsplash2.jpg")
    # отправляет фото в личку пользователю
    await bot.send_location(chat_id=message.from_user.id, latitude=55, longitude=65)
    # отправляет локацию с этими параметрами в личку



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup_, skip_updates=True)  # skip_updates=True позволяет пропускать
    # обновления которые произошли в офлайне,
    # бот не будет отвечать на те команды которые пользователь ввел пока бот не работал
