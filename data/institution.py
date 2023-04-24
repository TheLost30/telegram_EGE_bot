import re
import sqlite3

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler

from data.points import recognize_subject as rec_s

con = sqlite3.connect('data/institutions.db')
cur = con.cursor()


def get_from_db():
    tabs = ["специальность", "ВУЗ", "баллов на бюджет",
            "баллов на платное", "места бюджет", "места платно", "предметы", "сайт"]
    command = 'select * from specs'
    result = cur.execute(command).fetchall()
    result = [{tabs[i]: j for i, j in enumerate(k)} for k in result]
    for i in result:
        i['less'] = [j.split() for j in i['предметы'].split(' или ')]
        temp_sp = []
        for j in i['less']:
            if sum(i['less'].count(k) for k in j) == len(i['less']):
                temp_sp.append(j)
        # i['предметы'] = ', '.join()
    return result


async def find_inst(update, context):
    query = update.callback_query
    if query.data == "inst_points":
        if not any(context.user_data['points'].values()):
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Ввести", callback_data="set_points")],
                                             [InlineKeyboardButton("◀️ Вернуться", callback_data="find_institution")]])
            await context.bot.editMessageText(text=f'У вас нет сохранённых баллов, введите свои баллы',
                                              reply_markup=keyboard, chat_id=query.message.chat_id,
                                              message_id=query.message.message_id)
            return

    result = get_from_db()
    sp = []
    for i in result:
        _temp = max(sum(context.user_data['points'][rec_s(lesson)] for lesson in lessons)
                    + context.user_data['points'][rec_s('рус')] for lessons in i['less'])
        if _temp >= i['баллов на бюджет'] or _temp >= i['баллов на платное']:
            i.pop('less')
            sp.append(i)
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Вернуться", callback_data="find_institution")]])
    if not sp:
        await context.bot.editMessageText(text='По вашим баллам не удалось найти специальность, это возможно из-за:\n'
                                               '-Нехватки баллов для поступления\n'
                                               '-Не записаны баллы по дополнительным предметам,'
                                               ' кроме русского языка и математики',
                                          reply_markup=keyboard, chat_id=query.message.chat_id,
                                          message_id=query.message.message_id)
        return
    await context.bot.editMessageText(text='Специальности, на которые вы можете поступить\n\n'
                                           + '\n-----\n'.join(
        ['\n'.join([f'{i}: {j}' for i, j in k.items()]) for k in sp]),
                                      reply_markup=keyboard, chat_id=query.message.chat_id,
                                      message_id=query.message.message_id)


def set_institution_commands(app):
    app.add_handler(CallbackQueryHandler(find_inst, pattern=re.compile('inst_points')))
