import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions
from handlers import router
# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=os.environ.get("TOKEN"))
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!")

async def main():
    try:
        await dp.start_polling(bot)
    except exceptions.TelegramAPIError as e:
        logger.error(f"Telegram API Error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    asyncio.run(main())
