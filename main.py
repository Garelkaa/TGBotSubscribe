import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
import keyboard as key
from db import Database
import cfg 
from aiogram.dispatcher.filters import Text
import time
import datetime
logging.basicConfig(level=logging.INFO)

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)

database = Database('users.db')

def day_to_sec(days):
    return days * 24 * 60 * 60

def time_sub(gettime):
    timesSub = int(time.time())
    midtime = int(gettime) - timesSub

    if midtime <= 0:
        return False
    else:
        md = str(datetime.timedelta(seconds=midtime))
        md = md.replace('days', 'дней')
        return md 

@dp.message_handler(commands='start')
async def start_command(message: types.Message):
    if(not database.user_exists(message.from_user.id)):
        database.addUser(message.from_user.id)
        await bot.send_message(message.from_user.id, "Добро пожаловать!", reply_markup=key.main)
    else:
        return

@dp.callback_query_handler(text="mount")
async def subactivate(call: types.CallbackQuery):
    await bot.send_invoice(chat_id=call.from_user.id, title="Оформление", description='На месяц', payload="month", provider_token=cfg.OPLATA, currency="RUB", start_parameter="testik", prices=[{"label": "Руб", "amount": 10000}])
    
@dp.pre_checkout_query_handler()
async def process_pay(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def oplataqweqwe(message: types.Message):
    if message.successful_payment.invoice_payload == 'month':
        await bot.send_message(message.from_user.id, f"Оплата прошла успешно!\nВыдана подписка на месяц")
        timeSub = int(time.time()) + day_to_sec(30)
        database.settime(message.from_user.id, timeSub)

@dp.message_handler(Text('Подписка'))
async def subCheckPrice(message: types.Message):
    await bot.send_message(message.from_user.id, f"Сюда вписываем, что даёт подписка!", reply_markup=key.subInline)

@dp.message_handler(Text('Профиль'))
async def Profile(message: types.Message):
    userSubNow = time_sub(database.get_time(message.from_user.id))
    if userSubNow == False:
        userSubNow = "Нету подписки"
    
    userSubNow = "\n Осталось времени до отключения подписки:" + userSubNow
    await bot.send_message(message.from_user.id, #f"Ваш айди: {database.get_UserInfo}",
                            userSubNow)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)