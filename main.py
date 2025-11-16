import sys

import asyncio
from aiogram import types, F

import aiohttp
import logging

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton
from aiogram import html
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

bsn = '\n'
bsr = '\r'
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Здравствуй, {html.bold(message.from_user.full_name)}! \n Если вы это читаете, значит вы тестируете это чудо-юдо. \n Введите список сайтов (каждый с новой строки) для регулярного пинга из сети российского провайдера.")
    
@dp.message(Command("ping"))
async def ping(message: Message) -> None:
    usr_config = open(file=(f"user_data/{message.from_user.id}.txt"), mode='r')
    async with aiohttp.ClientSession(max_line_size=8190 * 2,  
        max_field_size=8190 * 2) as session:
        for line in usr_config:
            try:
                async with session.get(f'https://{line}', timeout=aiohttp.ClientTimeout(8)) as resp:
                    await message.answer(f"{line.replace(bsr, '').replace(bsn, '')} - доступ ({resp.status}) ✅")
            except Exception as e:
                await message.answer(f"{line.replace(bsr, '').replace(bsn, '')} - запрет ❌")

@dp.message()
async def list(message: Message) -> None:
    try:
        usr_config = open(file=(f"user_data/{message.from_user.id}.txt"), mode='w+')
        usr_config.write(str(message.text))
        usr_config.close()
        await message.reply("Список доменов успешно обновлён")
    except Exception as e:
        await message.reply(str(e))



async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())