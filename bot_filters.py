import asyncio
from aiogram import Bot, Dispatcher
from config_reader import config
from handlers import group_names, usernames, different_types, bot_in_group, events_in_group


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(group_names.router, different_types.router, group_names.router)
    #dp.include_routers(usernames.router)
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())