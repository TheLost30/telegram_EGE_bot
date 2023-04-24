import logging
import re

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from data import config as cfg
from data import institution as inst
from data import points


def check_points(user_data):
    if 'points' not in user_data.keys():
        user_data['points'] = {'Математика': 0, 'Русский язык': 0,
                               'Иностранный язык': 0, 'Физика': 0, 'Обществознание': 0, 'Химия': 0,
                               'История': 0, 'Биология': 0,
                               'Информатика': 0, 'Литература': 0, 'География': 0
                               }
    if 'temp_points' in user_data.keys():
        sp = {i: j for i, j in user_data['points'].items() if i not in user_data['temp_points'].keys()}
        sp = {**sp, **user_data['temp_points']}
        user_data['points'] = sp
    return user_data


async def start(update, context):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("📚 Управление баллами ЕГЭ", callback_data="ex_points")],
                                     [InlineKeyboardButton("🏫 Просмотр заведений",
                                                           callback_data="find_institution")]])
    context.user_data['points'] = check_points(context.user_data)['points']
    await update.message.reply_text(
        f'Привет, я бот "Калькулятор ЕГЭ", и я помогу найти тебе подходящий ВУЗ/институт.'
        f'Что вы желаете сделать сегодня?', reply_markup=keyboard)


async def help_buttons(update, context):
    query = update.callback_query
    logging.info(query)
    context.user_data['points'] = check_points(context.user_data)['points']
    keyboard = [InlineKeyboardButton("◀️ Вернуться", callback_data="start")]
    if query.data == "ex_points":
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Посмотреть", callback_data="get_points")],
                                         [InlineKeyboardButton("Изменить", callback_data="set_points")],
                                         [InlineKeyboardButton("Удалить", callback_data="del_points")],
                                         keyboard])
        await context.bot.editMessageText(text='Что вы желаете сделать со своими баллами ЕГЭ?',
                                          reply_markup=keyboard, chat_id=query.message.chat_id,
                                          message_id=query.message.message_id)

    elif query.data == "find_institution":
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("По баллам ЕГЭ", callback_data="inst_points")],
                                         keyboard])
        await context.bot.editMessageText(text="Просмотр заведений", reply_markup=keyboard,
                                          chat_id=query.message.chat_id, message_id=query.message.message_id)
    elif query.data == "start":
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("📚 Управление баллами ЕГЭ", callback_data="ex_points")],
                                         [InlineKeyboardButton("🏫 Просмотр заведений",
                                                               callback_data="find_institution")]])
        await context.bot.editMessageText(
            f'Привет, я бот "Калькулятор ЕГЭ", и я помогу найти тебе подходящий ВУЗ/институт. '
            f'Что вы желаете сделать сегодня?', reply_markup=keyboard,
            chat_id=query.message.chat_id, message_id=query.message.message_id)


def main():
    app = Application.builder().token(cfg.token).build()
    points.set_point_commands(app)
    inst.set_institution_commands(app)
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(help_buttons, pattern=re.compile('ex_points|find_institution|start')))

    app.run_polling()


if __name__ == '__main__':
    main()
