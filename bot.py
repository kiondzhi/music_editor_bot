import telebot
from telebot import types

# Токен телеграм бота
TOKEN = '7829141390:AAESO3tUmEebNfLdSg6xGEtSFwh2KTPG69c'
bot = telebot.TeleBot(TOKEN)

# Каналы с ID на которые нужно подписаться
CHANNELS = ['@thijaeiopthapeotjhteahte', '@second2fasgdsfsafdsa', '@three3gafdgfdsg']

# Сохранение выбранного языка в массив
user_languages = {}

# Переменные с сохранением ID сообщения
welcome_message_id = {}
subscribe_message_id = {}
not_subscribed_message_id = {}

# Обработка команды start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()

    # Кнопки выбора языка
    btn_rus = types.InlineKeyboardButton('🇷🇺 Русский', callback_data='language_rus')
    btn_eng = types.InlineKeyboardButton('🇺🇸 English', callback_data='language_eng')
    markup.add(btn_rus, btn_eng)

    # Выводим сообщение
    msg = bot.send_message(message.chat.id, "*Please select a language!*", reply_markup=markup, parse_mode='Markdown')

    # Сохраняем приветственное сообщение в массив
    welcome_message_id[message.chat.id] = msg.message_id

# Обработка выбора языка
@bot.callback_query_handler(func=lambda call: call.data in ['language_rus', 'language_eng'])
def handle_language_choice(call):
    language = '🇷🇺 Русский' if call.data == 'language_rus' else '🇺🇸 English'
    user_languages[call.from_user.id] = language # Сохраняем язык в переменной
    
    # Удаляем сообщение с выбором языка
    bot.delete_message(call.message.chat.id, welcome_message_id[call.message.chat.id])

    # Проверяем подписки
    check_subscribes(call.message, language)

# Проверяем подписки
def check_subscribes(message, language):
    markup = types.InlineKeyboardMarkup()

    # Добавляем кнопки для каждого канала
    if language == '🇷🇺 Русский':
        channel_one = types.InlineKeyboardButton("1 — Канал", url="https://t.me/+U0-oRzG5zeFjYjY6")
        channel_two = types.InlineKeyboardButton("2 — Канал", url="https://t.me/+rTQWzQy9sEc3ZWIy")
        channel_three = types.InlineKeyboardButton("3 — Канал", url="https://t.me/+pvesJQY0fzk2YzZi")
    elif language == '🇺🇸 English':
        channel_one = types.InlineKeyboardButton("1 — Channel", url="https://t.me/+U0-oRzG5zeFjYjY6")
        channel_two = types.InlineKeyboardButton("2 — Channel", url="https://t.me/+rTQWzQy9sEc3ZWIy")
        channel_three = types.InlineKeyboardButton("3 — Channel", url="https://t.me/+pvesJQY0fzk2YzZi")

    # Добавляем кнопки для проверки подписок
    if language == '🇷🇺 Русский':
        check_btn = types.InlineKeyboardButton("Проверить подписки", callback_data="check_subscription")
    elif language == '🇺🇸 English':
        check_btn = types.InlineKeyboardButton("Check subscriptions", callback_data="check_subscription")

    # Создаём кнопки
    markup.add(channel_one, channel_two, channel_three, check_btn)

    # Отправка сообщения с кнопками
    if language == '🇷🇺 Русский':
        msg = bot.send_message(message.chat.id, "*Чтобы продолжить, пожалуйста подпишитесь на каналы* 👇🏻", reply_markup=markup, parse_mode='Markdown')
    elif language == '🇺🇸 English':
        msg = bot.send_message(message.chat.id, "*To continue, please subscribe to the channels* 👇🏻", reply_markup=markup, parse_mode='Markdown')
    
    # Сохраняем сообщение о подписках на каналы в массив
    subscribe_message_id[message.chat.id] = msg.message_id

# Обработка проверки подписки
@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def verify_subscription(call):
    user_id = call.from_user.id
    subscribed_channels = is_user_subscribed(user_id)

    # Получаем язык выбранного сообщения из массива
    language = user_languages.get(user_id)

    if len(subscribed_channels) == len(CHANNELS):
        if language == '🇷🇺 Русский':
            bot.delete_message(call.message.chat.id, subscribe_message_id[call.message.chat.id]) # Удаляем менюшку о подписке на каналы
            bot.send_message(call.message.chat.id, "*Вы подписаны на все каналы! Теперь вы можете пользоваться этим ботом.*", parse_mode='Markdown')
        elif language == '🇺🇸 English':
            bot.delete_message(call.message.chat.id, subscribe_message_id[call.message.chat.id]) # Удаляем менюшку сообщение о подписке на каналы
            bot.send_message(call.message.chat.id, "*You are subscribed to all channels! Now you can use this bot.*", parse_mode='Markdown')
    else:
        not_subscribed = set(CHANNELS) - set(subscribed_channels)
        if language == '🇷🇺 Русский':
            not_subscribed_msg = bot.send_message(call.message.chat.id, f"*Вы не подписаны на следующие каналы: {', '.join(not_subscribed)}.\nПожалуйста, подпишитесь на них, чтобы получить доступ к боту.*", parse_mode='Markdown')
            not_subscribed_message_id[call.message.chat.id] = not_subscribed_msg.message_id # Сохраняем ID сообщения о не подписке на каналы
        elif language == '🇺🇸 English':
            not_subscribed_msg = bot.send_message(call.message.chat.id, f"*You are not subscribed to the following channels: {', '.join(not_subscribed)}.\nPlease subscribe to them to get access to the bot.*", parse_mode='Markdown')
            not_subscribed_message_id[call.message.chat.id] = not_subscribed_msg.message_id # Сохраняем ID сообщения о не подписке на каналы

    # Если пользователь подписался, удаляем сообщение о неподписке
    if len(subscribed_channels) == len(CHANNELS) and call.message.chat.id in not_subscribed_message_id: 
        bot.delete_message(call.message.chat.id, not_subscribed_message_id[call.message.chat.id]) 
        del not_subscribed_message_id[call.message.chat.id] # Удаляем ID сообщения о не подписке на каналы

# Проверка подписки
def is_user_subscribed(user_id):
    subscribed = []
    for channel in CHANNELS:
        try:
            chat_member = bot.get_chat_member(channel, user_id)
            if chat_member.status in ['member', 'administrator', 'creator']:
                subscribed.append(channel)
        except Exception as e:
            print(f"Ошибка проверки подписки на {channel}: {e}")
    return subscribed

# Запуск бота
bot.infinity_polling()