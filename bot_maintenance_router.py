import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import MagicData, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_reader import config

# Создаём роутер для режима обслуживания и ставим ему фильтры на типы
maintenance_router = Router()
maintenance_router.message.filter(MagicData(F.maintenance_mode.is_(True)))
maintenance_router.callback_query.filter(MagicData(F.maintenance_mode.is_(True)))

regular_router = Router()

# Хэндлеры этого роутера перехватят все сообщения и колбэки,
# если maintenance_mode равен True
@maintenance_router.message()
async def any_message(message: Message):
    await message.answer("Бот в режиме обслуживания. Пожалуйста, подождите.")


@maintenance_router.callback_query()
async def any_callback(callback: CallbackQuery):
    await callback.answer(
        text="Бот в режиме обслуживания. Пожалуйста, подождите",
        show_alert=True
    )

# Хэндлеры этого роутера используются ВНЕ режима обслуживания,
# т.е. когда maintenance_mode равен False или не указан вообще
@regular_router.message(CommandStart())
async def cmd_start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Нажми меня", callback_data="anything")
    await message.answer(
        text="Какой-то текст с кнопкой",
        reply_markup=builder.as_markup()
    )


@regular_router.callback_query(F.data == "anything")
async def callback_anything(callback: CallbackQuery):
    await callback.answer(
        text="Это какое-то обычное действие",
        show_alert=True
    )


async def main() -> None:
    bot = Bot(token=config.bot_token.get_secret_value())
    # В реальной жизни значение maintenance_mode
    # будет взято из стороннего источника (например, конфиг или через API)
    # Помните, что т.к. bool тип является иммутабельным,
    # его смена в рантайме ни на что не повлияет
    dp = Dispatcher(maintenance_mode=True)
    # Maintenance-роутер должен быть первый
    dp.include_routers(maintenance_router, regular_router)
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())