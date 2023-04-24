import re

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, filters


def recognize_subject(subject: str, value='text'):
    match value:
        case 'data':
            subject_patterns = {
                'mat': r'мат(ематика)?',
                'rus': r'рус(ский\sязык)?',
                'inos': r'(английский|китайский|французкий|японский|немецкий|иностранный)\s?(язык)?',
                'fiz': r'физ(ика)?',
                'obsh': r'общ(ествознание)?',
                'him': r'хим(ия)?',
                'ist': r'история',
                'bio': r'биол(огия)?',
                'inf': r'инф(орматика)?',
                'lit': r'лит(ература)?',
                'geo': r'геогр(афия)?'
            }
        case 'all':
            subject_patterns = {
                ['Математика', 'mat']: r'мат(ематика)?',
                ['Русский язык', 'rus']: r'рус(ский\sязык)?',
                ['Иностранный язык', 'inos']: r'(английский|китайский|французкий|'
                                              r'японский|немецкий|иностранный)\s?(язык)?',
                ['Физика', 'fiz']: r'физ(ика)?',
                ['Обществознание', 'obsh']: r'общ(ествознание)?',
                ['Химия', 'him']: r'хим(ия)?',
                ['История', 'ist']: r'история',
                ['Биология', 'bio']: r'биол(огия)?',
                ['Информатика', 'inf']: r'инф(орматика)?',
                ['Литература', 'lit']: r'лит(ература)?',
                ['География', 'geo']: r'геогр(афия)?'
            }
        case _:
            subject_patterns = {
                'Информатика': r'инф(орматика)?',
                'Математика': r'мат(ематика)?',
                'Русский язык': r'рус(ский\sязык)?',
                'Физика': r'физ(ика)?',
                'Обществознание': r'общ(ествознание)?',
                'Химия': r'хим(ия)?',
                'История': r'ист(ория)?',
                'Биология': r'био(логия)?',
                'Литература': r'лит(ература)?',
                'География': r'гео(графия)?',
                'Иностранный язык': r'(английский|китайский|французкий|японский|немецкий|иностранный)?'
            }

    for key, pattern in subject_patterns.items():
        if re.search(pattern, subject, re.IGNORECASE):
            return key

    return None


def declension(number):
    if number % 10 == 1 and number % 100 != 11:
        return 'балл'
    elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return 'балла'
    else:
        return 'баллов'


async def command(update, context):
    query = update.callback_query
    if query.data == 'get_points':
        if any(context.user_data['points'].values()):
            points = context.user_data['points']
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('◀️ Вернуться', callback_data='ex_points')]])
            await context.bot.editMessageText(text=f'Ваши баллы ЕГЭ:\n' +
                                                   '\n'.join(f'{i}: {j} баллов'
                                                             for i, j in points.items() if j > 0),
                                              reply_markup=keyboard, chat_id=query.message.chat_id,
                                              message_id=query.message.message_id)
        else:
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Ввести', callback_data='set_points')],
                                             [InlineKeyboardButton('◀️ Вернуться', callback_data='ex_points')]])
            await context.bot.editMessageText(text=f'У вас нет сохранённых баллов, введите свои баллы',
                                              reply_markup=keyboard, chat_id=query.message.chat_id,
                                              message_id=query.message.message_id)
    elif query.data == 'set_points':
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('✏️Написать', callback_data='all')],
                                         [InlineKeyboardButton('➕Математика', callback_data='мат')],
                                         [InlineKeyboardButton('🌐Язык', callback_data='None1')],
                                         [InlineKeyboardButton('🇷🇺Русский', callback_data='рус'),
                                          InlineKeyboardButton('🇱🇷Иностранный', callback_data='англ')],
                                         [InlineKeyboardButton('Доп. предметы', callback_data='None2')],
                                         [InlineKeyboardButton('💡Физика', callback_data='физ'),
                                          InlineKeyboardButton('🖥Информатика', callback_data='инф')],
                                         [InlineKeyboardButton('🧪Химия', callback_data='хим'),
                                          InlineKeyboardButton('🧬Биология', callback_data='биол')],
                                         [InlineKeyboardButton('📕История', callback_data='ист'),
                                          InlineKeyboardButton('🌍Георгафия', callback_data='гео')],
                                         [InlineKeyboardButton('📗Обществознание', callback_data='общ'),
                                          InlineKeyboardButton('📖Литература', callback_data='лит')],
                                         [InlineKeyboardButton('◀️ Вернуться', callback_data='ex_points')]])
        await context.bot.editMessageText(text='Какие баллы хотите изменить?',
                                          reply_markup=keyboard, chat_id=query.message.chat_id,
                                          message_id=query.message.message_id)
    elif query.data == 'del_points':
        context.user_data['points'] = {'Математика': 0, 'Русский язык': 0,
                               'Иностранный язык': 0, 'Физика': 0, 'Обществознание': 0, 'Химия': 0,
                               'История': 0, 'Биология': 0,
                               'Информатика': 0, 'Литература': 0, 'География': 0
                               }
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('◀️ Вернуться', callback_data='ex_points')]])
        await context.bot.editMessageText(text='Баллы ЕГЭ успешно удалены',
                                          reply_markup=keyboard, chat_id=query.message.chat_id,
                                          message_id=query.message.message_id)
    return ConversationHandler.END


async def choose_set_points(update, context):
    query = update.callback_query
    if query.data == 'all':
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('◀️ Вернуться', callback_data='set_points')]])
        await context.bot.editMessageText(text='Напишите Баллы ЕГЭ используя формат:\n'
                                               'Профильная математика - 10\n'
                                               'Русский язык - 15',
                                          reply_markup=keyboard, chat_id=query.message.chat_id,
                                          message_id=query.message.message_id)
        return 'all'
    else:
        subject = recognize_subject(query.data)
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('◀️ Вернуться', callback_data='set_points')]])
        await context.bot.editMessageText(text=f'Напишите Баллы ЕГЭ по предмету {subject}',
                                          reply_markup=keyboard, chat_id=query.message.chat_id,
                                          message_id=query.message.message_id)
        context.user_data['temp_subject'] = subject
        return 'one'


async def set_one_points(update, context):
    subject = context.user_data['temp_subject']
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('◀️ Вернуться', callback_data='ex_points')]])
    try:
        points = int(update.message.text)
        if not (0 < points <= 100):
            raise ValueError
        context.user_data['points'][subject] = int(update.message.text)
    except ValueError:
        await update.message.reply_text(text='пожалуйста, запишите только число от 1 до 100',
                                        reply_markup=keyboard)
        return 'one'

    await update.message.reply_text(text=f'По предмету {subject} теперь {points} {declension(points)}',
                                    reply_markup=keyboard)
    return ConversationHandler.END


async def set_all_points(update, context):
    sp = {}
    points = update.message.text.split('\n')
    context.user_data['temp_points'] = {}
    for i in points:
        i = i.split('-')
        context.user_data['temp_points'][recognize_subject(i[0])] = int(i[1])

    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Верно', callback_data='start')],
                                     [InlineKeyboardButton('Изменить', callback_data='set_points')]])
    await update.message.reply_text(text=f'Убедитесь, правильно ли введены баллы ЕГЭ:\n' +
                                         '\n'.join(f'{i}: {j} {declension(int(j))}' for i, j in
                                                   context.user_data['temp_points'].items() if j != 0)
                                         + '\n\nЕсли что-то не так, то вы можете поменять каждый балл отдельно.',
                                    reply_markup=keyboard)
    return ConversationHandler.END


def set_point_commands(app):
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(choose_set_points, pattern=re.compile(r'мат|рус|англ|физ|'
                                                                                 'общ|хим|ист|биол|инф|лит|гео|all')),
                      CallbackQueryHandler(command, pattern=re.compile('get_points|set_points|del_points'))],
        states={
            'all': [MessageHandler(filters.TEXT & ~filters.COMMAND, set_all_points)],
            'one': [MessageHandler(filters.TEXT & ~filters.COMMAND, set_one_points)]
        },
        fallbacks=[CallbackQueryHandler(command, pattern=re.compile('get_points|set_points|del_points'))]
    )
    app.add_handler(conv_handler)
