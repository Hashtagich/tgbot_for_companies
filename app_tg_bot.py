import os

import telebot
from telebot import types

from token_and_text import *

#    Исправить опечатки в тексте, посмотреть как оптимизировать код с помощью словаря т к много повторяющихся элифов и доделать разджел Личные навнавыки, доработать команду / инфоыки

# Попробуйте ввести в Terminal вот это, если код бота не заработает:
# pip3 uninstall telebot
# pip3 uninstall PyTelegramBotAPI
# pip3 install pyTelegramBotAPI
# pip3 install --upgrade pyTelegramBotAPI

bot = telebot.TeleBot(token_bot)

name_company, name_representative, email, phone_num, text_read = '', '', '', '', ''


@bot.message_handler(commands=['help'])
def help_me(message):
    bot.send_message(message.from_user.id, help_text)


@bot.message_handler(commands=['start'])
def start_conversation(message):
    """Функция активируется при вводе /start и предлагает юзеру познакомиться."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton(meet)
    item2 = types.KeyboardButton(info_author)
    item3 = types.KeyboardButton(connection_author)

    markup.add(item1, item2, item3)
    bot.send_message(message.from_user.id, text='Начнём', reply_markup=markup)

    keyboard = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    btn_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(btn_yes, btn_no)

    bot.send_message(message.from_user.id, greeting, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    """Активация кнопок меню. Каждая кнопка либо создаёт новые кнопки меню либо выводит текст."""
    global text_read
    if message.chat.type == 'private':
        if message.text == meet:
            keyboard = types.InlineKeyboardMarkup()
            btn_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
            btn_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
            keyboard.add(btn_yes, btn_no)

            bot.send_message(message.from_user.id, greeting, reply_markup=keyboard)

        elif message.text == info_author or message.text == info_author_back:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            item1 = types.KeyboardButton(knowledge_py)
            item2 = types.KeyboardButton(last_work)
            item3 = types.KeyboardButton(personal_skills)
            item4 = types.KeyboardButton(goals_tasks)
            back_btn = types.KeyboardButton(back)
            markup.add(item1, item2, item3, item4, back_btn)
            bot.send_message(message.from_user.id, info_author, reply_markup=markup)

        elif message.text == knowledge_py:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            item1 = types.KeyboardButton('Пройденные курсы и сертификаты')
            item2 = types.KeyboardButton('Кратко о том что знает')
            item3 = types.KeyboardButton('Учебный план')
            item4 = types.KeyboardButton('Проекты')
            back_btn = types.KeyboardButton(info_author_back)
            markup.add(item1, item2, item3, item4, back_btn)
            bot.send_message(message.from_user.id, knowledge_py, reply_markup=markup)

        elif message.text == 'Пройденные курсы и сертификаты':
            text_read = text_completed_course_1
            keyboard = types.InlineKeyboardMarkup()
            btn_read = types.InlineKeyboardButton(text=btn_read_please, callback_data='btn_read_please')
            keyboard.add(btn_read)
            bot.send_message(message.from_user.id, text=text_read, reply_markup=keyboard)
            bot.send_message(message.from_user.id, text_completed_course_2)

            for filename in os.listdir(path_certificate):
                with open(os.path.join(path_certificate, filename), 'rb') as file_pdf:
                    bot.send_document(message.from_user.id, document=file_pdf)

        elif message.text == 'Кратко о том что знает':
            text_read = text_knowledge
            keyboard = types.InlineKeyboardMarkup()
            btn_read = types.InlineKeyboardButton(text=btn_read_please, callback_data='btn_read_please')
            keyboard.add(btn_read)
            bot.send_message(message.from_user.id, text=text_read, reply_markup=keyboard)

        elif message.text == 'Учебный план':
            text_read = text_training_plan
            keyboard = types.InlineKeyboardMarkup()
            btn_read = types.InlineKeyboardButton(text=btn_read_please, callback_data='btn_read_please')
            keyboard.add(btn_read)
            bot.send_message(message.from_user.id, text=text_read, reply_markup=keyboard)

        elif message.text == 'Проекты':
            text_read = text_project
            keyboard = types.InlineKeyboardMarkup()
            btn_read = types.InlineKeyboardButton(text=btn_read_please, callback_data='btn_read_please')
            keyboard.add(btn_read)
            bot.send_message(message.from_user.id, text=text_read, reply_markup=keyboard)
            bot.send_message(message.from_user.id, text=text_project_1)

        elif message.text == goals_tasks:
            text_read = target_goal
            keyboard = types.InlineKeyboardMarkup()
            btn_read = types.InlineKeyboardButton(text=btn_read_please, callback_data='btn_read_please')
            keyboard.add(btn_read)
            bot.send_message(message.from_user.id, text=text_read, reply_markup=keyboard)

        elif message.text == last_work:
            text_read = text_last_work
            keyboard = types.InlineKeyboardMarkup()
            btn_read = types.InlineKeyboardButton(text=btn_read_please, callback_data='btn_read_please')
            keyboard.add(btn_read)
            bot.send_message(message.from_user.id, text=text_read, reply_markup=keyboard)

        elif message.text == back:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            item1 = types.KeyboardButton(meet)
            item2 = types.KeyboardButton(info_author)
            item3 = types.KeyboardButton(connection_author)

            markup.add(item1, item2, item3)
            bot.send_message(message.from_user.id, text=back, reply_markup=markup)

        elif message.text == connection_author:
            bot.send_message(message.chat.id, connect_information)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'yes':
        bot.send_message(call.message.chat.id, text_i_know_you)
        # написать условие если есть имя компании в файле, то писать что знаешь если нет то знакомимся заново
        bot.send_message(call.message.chat.id, what_name)
        bot.register_next_step_handler(call.message, find_name)

    elif call.data == 'no':
        bot.send_message(call.message.chat.id, text_i_know_no)
        bot.send_message(call.message.chat.id, what_name)
        bot.register_next_step_handler(call.message, reg_name)

    elif call.data == 'yes_reg':
        bot.send_message(call.message.chat.id, reg_success)
        text_info = f'{name_company},{name_representative},{phone_num},{email},{call.message.from_user.id},' \
                    f'{call.message.from_user.first_name},{call.message.from_user.last_name},' \
                    f'{call.message.from_user.username}\n'  # для txt файла
        # text_info = [name_company, name_representative, phone_num, email, call.message.from_user.id,
        #              call.message.from_user.first_name, call.message.from_user.last_name,
        #              call.message.from_user.username]

        write_info(text_info)

    elif call.data == 'no_reg':
        bot.send_message(call.message.chat.id, "Хорошо, начнём с начала.")
        bot.send_message(call.message.chat.id, what_name)
        bot.register_next_step_handler(call.message, reg_name)

    elif call.data == 'btn_read_please':
        read_text(text_read)


def find_name(message):
    global name_representative
    name_representative = message.text
    bot.send_message(message.from_user.id, what_company)
    bot.register_next_step_handler(message, find_company)


def find_company(message):
    global name_company
    dict_companies = look_in_notebook(name_txt_file)
    name_company = message.text
    if name_company.lower() in dict_companies['name_company']:

        if name_representative in dict_companies['name_representative']:
            index_for_name_representative = dict_companies['name_company'].index(name_company.lower())
            find_name_representative = dict_companies['name_representative'][index_for_name_representative].title()
            bot.send_message(message.from_user.id,
                             f'Я нашел Ваше имя в своей записной книжке. Здравствуйте, {find_name_representative}')
        else:
            bot.send_message(message.from_user.id, i_not_find_name)
    else:
        bot.send_message(message.from_user.id, i_not_find_company)


def reg_name(message):
    global name_representative
    name_representative = message.text
    bot.send_message(message.from_user.id, what_company)
    bot.register_next_step_handler(message, reg_company)


def reg_company(message):
    global name_company
    name_company = message.text
    bot.send_message(message.from_user.id, what_phone_num)
    bot.register_next_step_handler(message, reg_phone_num)


def reg_phone_num(message):
    global phone_num
    phone_num = message.text
    bot.send_message(message.from_user.id, what_email)
    bot.register_next_step_handler(message, reg_ok)


def reg_ok(message):
    global email
    email = message.text
    bot.send_message(message.from_user.id, text=f'''Вас зовут {name_representative}
Контактный телефон: {phone_num}
Почта: {email}
Компания: {name_company}''')
    keyboard_reg = types.InlineKeyboardMarkup()

    btn_yes_reg = types.InlineKeyboardButton(text='Да', callback_data='yes_reg')
    btn_no_reg = types.InlineKeyboardButton(text='Нет', callback_data='no_reg')
    keyboard_reg.add(btn_yes_reg, btn_no_reg)

    bot.send_message(message.from_user.id, 'Верно?', reply_markup=keyboard_reg)


bot.polling(none_stop=True)
