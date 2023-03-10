import os

import telebot
from telebot import types
from notifiers import get_notifier

from token_and_text import *

# Попробуйте ввести в Terminal вот это, если код бота не заработает:
# pip3 uninstall telebot
# pip3 uninstall PyTelegramBotAPI
# pip3 install pyTelegramBotAPI
# pip3 install --upgrade pyTelegramBotAPI

bot = telebot.TeleBot(data['token_bot'])
telegram = get_notifier('telegram')


@bot.message_handler(commands=['help'])
def help_me(message) -> None:
    """Функция выводит информационное сообщение."""
    bot.send_message(message.from_user.id, data['help_text'])


@bot.message_handler(commands=['info'])
def info_me(message) -> None:
    """Функция выводит информацию о разработчике и отправляет разработчику информацию о том кто общается с ботом."""
    bot.send_message(message.chat.id, data['connect_information'])
    message_to_me = f"""Мне только что написали.
    Вот информация:
        ID: {message.from_user.id};
        FIRST_NAME: {message.from_user.first_name};
        LAST_NAME: {message.from_user.last_name};
        USERNAME: {message.from_user.username}."""

    telegram.notify(token=data['token_bot'], chat_id=data["user_id"], message=message_to_me)


@bot.message_handler(commands=['start'])
def start_conversation(message) -> None:
    """Функция активируется при вводе /start и предлагает юзеру познакомиться."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton(data['meet'])
    item2 = types.KeyboardButton(data['info_author'])
    item3 = types.KeyboardButton(data['connection_author'])

    markup.add(item1, item2, item3)
    bot.send_message(message.from_user.id, text='Начнём', reply_markup=markup)

    keyboard = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    btn_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(btn_yes, btn_no)

    bot.send_message(message.from_user.id, data['greeting'], reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def bot_message(message) -> None:
    """Активация кнопок меню. Каждая кнопка либо создаёт новые кнопки меню либо выводит текст."""
    global text_read
    if message.chat.type == 'private':

        for key, value in dict_command.items():
            if message.text == key:
                text_read = value
                keyboard = types.InlineKeyboardMarkup()
                # btn_read = types.InlineKeyboardButton(text=data['btn_read_please'], callback_data='btn_read_please')
                # keyboard.add(btn_read)
                bot.send_message(message.from_user.id, text=text_read, reply_markup=keyboard)

        if message.text == data['meet']:
            keyboard = types.InlineKeyboardMarkup()
            btn_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
            btn_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
            keyboard.add(btn_yes, btn_no)

            bot.send_message(message.from_user.id, data['greeting'], reply_markup=keyboard)

        elif message.text == data['info_author'] or message.text == data['info_author_back']:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            item1 = types.KeyboardButton(data['knowledge_py'])
            item2 = types.KeyboardButton(data['last_work'])
            item3 = types.KeyboardButton(data['personal_skills'])
            item4 = types.KeyboardButton(data['goals_tasks'])
            back_btn = types.KeyboardButton(data['back'])
            markup.add(item1, item2, item3, item4, back_btn)
            bot.send_message(message.from_user.id, data['info_author'], reply_markup=markup)

        elif message.text == data['knowledge_py']:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            item1 = types.KeyboardButton('Пройденные курсы и сертификаты')
            item2 = types.KeyboardButton('Кратко о том что знает')
            item3 = types.KeyboardButton('Учебный план')
            item4 = types.KeyboardButton('Проекты')
            back_btn = types.KeyboardButton(data['info_author_back'])
            markup.add(item1, item2, item3, item4, back_btn)
            bot.send_message(message.from_user.id, data['knowledge_py'], reply_markup=markup)

        elif message.text == 'Пройденные курсы и сертификаты':
            text_read = data['text_completed_course_1']
            keyboard = types.InlineKeyboardMarkup()
            # btn_read = types.InlineKeyboardButton(text=data['btn_read_please'], callback_data='btn_read_please')
            # keyboard.add(btn_read)
            bot.send_message(message.from_user.id, text=text_read, reply_markup=keyboard)
            bot.send_message(message.from_user.id, data['text_completed_course_2'])

            for filename in os.listdir(path_certificate):
                with open(os.path.join(path_certificate, filename), 'rb') as file_pdf:
                    bot.send_document(message.from_user.id, document=file_pdf)

        elif message.text == 'Проекты':
            text_read = data['text_project']
            keyboard = types.InlineKeyboardMarkup()
            # btn_read = types.InlineKeyboardButton(text=data['btn_read_please'], callback_data='btn_read_please')
            # keyboard.add(btn_read)
            bot.send_message(message.from_user.id, text=text_read, reply_markup=keyboard)
            bot.send_message(message.from_user.id, text=data['text_project_1'])

        elif message.text == data['back']:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            item1 = types.KeyboardButton(data['meet'])
            item2 = types.KeyboardButton(data['info_author'])
            item3 = types.KeyboardButton(data['connection_author'])

            markup.add(item1, item2, item3)
            bot.send_message(message.from_user.id, text=data['back'], reply_markup=markup)

        elif message.text == data['connection_author']:
            info_me(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call) -> None:
    """Функция ищет пользователя в базе, запускает процесс регистрации или сохраняет данные пользователя
    и отправляет разработчику информацию в зависимости от выбранного варианта."""
    if call.data == 'yes':
        bot.send_message(call.message.chat.id, data['text_i_know_you'])
        bot.send_message(call.message.chat.id, data['what_name'])
        bot.register_next_step_handler(call.message, find_name)

    elif call.data == 'no':
        bot.send_message(call.message.chat.id, data['text_i_know_no'])
        bot.send_message(call.message.chat.id, data['what_name'])
        bot.register_next_step_handler(call.message, reg_name)

    elif call.data == 'yes_reg':
        bot.send_message(call.message.chat.id, data['reg_success'])
        text_info = f'{name_company},{name_representative},{phone_num},{email},{list_user_info[0]},' \
                    f'{list_user_info[1]},{list_user_info[2]},' \
                    f'{list_user_info[3]}\n'  # для txt файла

        message_to_me = f"""Со мной познакомились. 
Вот информация: 
Название компании: {name_company};
Представитель: {name_representative};
Номер телефона: {phone_num};
Почта: {email};

ID: {list_user_info[0]};
FIRST_NAME: {list_user_info[1]};
LAST_NAME: {list_user_info[2]};
USERNAME: {list_user_info[3]}."""

        telegram.notify(token=data['token_bot'], chat_id=data["user_id"], message=message_to_me)
        write_info(text_info)

    elif call.data == 'no_reg':
        bot.send_message(call.message.chat.id, "Хорошо, начнём с начала.")
        bot.send_message(call.message.chat.id, data['what_name'])
        bot.register_next_step_handler(call.message, reg_name)

    # elif call.data == 'btn_read_please':
    #     read_text(text_read)


def find_name(message) -> None:
    """Функция принимает сообщение от пользователя и переходит к следующей функции find_company."""
    global name_representative
    name_representative = message.text
    bot.send_message(message.from_user.id, data['what_company'])
    bot.register_next_step_handler(message, find_company)


def find_company(message) -> None:
    """Функция принимает сообщение от пользователя и проверяет наличия имени представителя и название компании,
    по результатам выдаёт соответсвующий ответ."""
    global name_company
    dict_companies = look_in_notebook(name_txt_file)
    name_company = message.text
    if name_company.lower() in dict_companies['name_company']:

        if name_representative.lower() in dict_companies['name_representative']:
            # index_for_name_representative = dict_companies['name_company'].index(name_company.lower())
            # find_name_representative = dict_companies['name_representative'][index_for_name_representative].title()
            bot.send_message(message.from_user.id,
                             f'Я нашел Ваше имя в своей записной книжке. Здравствуйте, {name_representative}')
        else:
            bot.send_message(message.from_user.id, data['i_not_find_name'])
    else:
        bot.send_message(message.from_user.id, data['i_not_find_company'])


def reg_name(message) -> None:
    """Функция принимает сообщение от пользователя и переходит к следующей функции reg_company."""
    global name_representative
    name_representative = message.text
    bot.send_message(message.from_user.id, data['what_company'])
    bot.register_next_step_handler(message, reg_company)


def reg_company(message) -> None:
    """Функция принимает сообщение от пользователя и переходит к следующей функции reg_phone_num."""
    global name_company
    name_company = message.text
    bot.send_message(message.from_user.id, data['what_phone_num'])
    bot.register_next_step_handler(message, reg_phone_num)


def reg_phone_num(message) -> None:
    """Функция принимает сообщение от пользователя и переходит к следующей функции reg_ok."""
    global phone_num
    phone_num = message.text
    bot.send_message(message.from_user.id, data['what_email'])
    bot.register_next_step_handler(message, reg_ok)


def reg_ok(message) -> None:
    """Функция уточняет вся ли информация переданная из функция reg_company, reg_phone_num, reg_name верна."""
    global email, list_user_info
    email = message.text
    bot.send_message(message.from_user.id, text=f'''Вас зовут {name_representative}
Контактный телефон: {phone_num}
Почта: {email}
Компания: {name_company}''')

    list_user_info = [message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                      message.from_user.username]
    keyboard_reg = types.InlineKeyboardMarkup()

    btn_yes_reg = types.InlineKeyboardButton(text='Да', callback_data='yes_reg')
    btn_no_reg = types.InlineKeyboardButton(text='Нет', callback_data='no_reg')
    keyboard_reg.add(btn_yes_reg, btn_no_reg)

    bot.send_message(message.from_user.id, 'Верно?', reply_markup=keyboard_reg)


bot.polling(none_stop=True)
