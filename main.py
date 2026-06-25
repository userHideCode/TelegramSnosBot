import asyncio, aiogram, os, dotenv
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.handlers import rt

load_dotenv(".env")

bot = Bot(token=str(os.getenv('TOKEN')))
dp = Dispatcher()

async def main():
	dp.include_router(rt)
	
	await dp.start_polling(bot)
	
if __name__ == "__main__":
	try:
		asyncio.run(main())
		print("Бот запущен.")
	except Exception as e:
		print("Критическая ошибка:\n\n" + e)