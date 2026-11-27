import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = {int(x.strip()) for x in os.getenv('ADMIN_IDS', '').split(',') if x.strip().isdigit()}
PORT = int(os.getenv('PORT', '10000'))

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Welcome!\n\n"
        "This bot is online. Use /help to see available commands."
    )

@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer('/start — Start the bot\n/help — Show help\n/id — Show your Telegram user ID')

@router.message(Command('id'))
async def show_id(message: Message):
    await message.answer(f'Your Telegram user ID: <code>{message.from_user.id}</code>')

@router.message(Command('admin'))
async def admin(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer('You are not authorized to use admin commands.')
        return
    await message.answer('Admin access verified. Admin tools can be added here.')

async def health(request):
    return web.Response(text='ok')

async def main():
    if not BOT_TOKEN:
        raise RuntimeError('BOT_TOKEN environment variable is missing')
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    app = web.Application()
    app.router.add_get('/', health)
    app.router.add_get('/health', health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    log.info('Health server listening on port %s', PORT)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await runner.cleanup()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
