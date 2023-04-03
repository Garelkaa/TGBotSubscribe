from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

mainBtn = [
    [
        KeyboardButton('Подписка'),
        KeyboardButton('Профиль')
    ]
]

main = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=mainBtn)

subInline = InlineKeyboardMarkup(row_width=1)

btnSub = InlineKeyboardButton(text='Подписка на месяц', callback_data="mount")

subInline.insert(btnSub)