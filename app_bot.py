import os
from random import randint, sample

import requests
import telebot
from geopy import geocoders
from notifiers import get_notifier
from telebot import types

from token_and_text import *

# Попробуйте ввести в Terminal вот это, если код бота не заработает:
# pip3 uninstall telebot
# pip3 uninstall PyTelegramBotAPI
# pip3 install pyTelegramBotAPI
# pip3 install --upgrade pyTelegramBotAPI

bot = telebot.TeleBot(data['token_bot'])
telegram = get_notifier('telegram')

dict_conditions_ru = data["data_weather"]["conditions_ru"]
dict_part_name_ru = data["data_weather"]["part_name_ru"]


@bot.message_handler(commands=['help'])
def help_me(message) -> None:
    """Функция выводит информационное сообщение."""
    bot.send_message(message.from_user.id, data['help_text'])


@bot.message_handler(commands=['info'])
def info_me(message) -> None:
    """Функция выводит информацию о разработчике и отправляет разработчику информацию о том кто общается с ботом."""
    bot.send_message(message.chat.id, data['connect_information'])
    message_to_me = f"Мне только что написали. {get_info(message)}"
    telegram.notify(token=data['token_bot'], chat_id=data["user_id"], message=message_to_me)

    write_info(get_text_for_write(message) + ', Info\n')


@bot.message_handler(commands=['start'])
def start_conversation(message) -> None:
    """Функция активируется при вводе /start и отправляет уведомление разработчику, что бота активировали
    и записывает в базу данных информацию о написавшем."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton(data['simple_move'])
    item2 = types.KeyboardButton(data['info_author'])
    item3 = types.KeyboardButton(data['connection_author'])

    markup.add(item2, item3, item1)
    bot.send_message(message.from_user.id, text='Начнём', reply_markup=markup)

    message_to_me = f"Меня активировали. {get_info(message)}"
    telegram.notify(token=data['token_bot'], chat_id=data["user_id"], message=message_to_me)

    write_info(get_text_for_write(message) + ', Start\n')


@bot.message_handler(content_types=['text'])
def bot_message(message) -> None:
    """Активация кнопок меню. Каждая кнопка либо создаёт новые кнопки меню либо выводит текст."""

    if message.chat.type == 'private':

        result_0 = dict_command.get(message.text, False)
        if result_0:
            keyboard = types.InlineKeyboardMarkup()
            bot.send_message(message.from_user.id, text=result_0, reply_markup=keyboard)

        result = db_buttons.get(message.text, False)
        if result:
            result(message)


# Функции для словаря db_buttons


def info_author(message) -> None:
    """Функция изменяет кнопки для раздела 'О разработчике'."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton(data['knowledge_py'])
    item2 = types.KeyboardButton(data['last_work'])
    item3 = types.KeyboardButton(data['personal_skills'])
    item4 = types.KeyboardButton(data['goals_tasks'])
    back_btn = types.KeyboardButton(data['back'])
    markup.add(item1, item2, item3, item4, back_btn)
    bot.send_message(message.from_user.id, data['info_author'], reply_markup=markup)


def simple_move(message) -> None:
    """Функция изменяет кнопки для раздела 'Простые действия'."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton(data['coin'])
    item2 = types.KeyboardButton(data['rand_int'])
    item3 = types.KeyboardButton(data['weather_report'])
    item4 = types.KeyboardButton(data['simple_list'])
    back_btn = types.KeyboardButton(data['back'])
    markup.add(item1, item2, item3, item4, back_btn)
    bot.send_message(message.from_user.id, data['simple_move'], reply_markup=markup)


def knowledge_py(message) -> None:
    """Функция изменяет кнопки для раздела 'Знание питона'."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('Пройденные курсы и сертификаты')
    item2 = types.KeyboardButton('Кратко о том что знает')
    item3 = types.KeyboardButton('Учебный план')
    item4 = types.KeyboardButton('Проекты')
    back_btn = types.KeyboardButton(data['info_author_back'])
    markup.add(item1, item2, item3, item4, back_btn)
    bot.send_message(message.from_user.id, data['knowledge_py'], reply_markup=markup)


def course_and_certificate(message) -> None:
    """Функция отправляет информацию и сертификаты в чат о пройденных курсах."""
    text_read = data['text_completed_course_1']
    keyboard = types.InlineKeyboardMarkup()

    bot.send_message(message.from_user.id, text=text_read, reply_markup=keyboard)
    bot.send_message(message.from_user.id, data['text_completed_course_2'])

    for filename in os.listdir(path_certificate):
        with open(os.path.join(path_certificate, filename), 'rb') as file_pdf:
            bot.send_document(message.from_user.id, document=file_pdf)


def project(message) -> None:
    """Функция отправляет информацию в чат о проектах."""
    text_read = data['text_project']
    keyboard = types.InlineKeyboardMarkup()

    bot.send_message(message.from_user.id, text=text_read, reply_markup=keyboard)
    bot.send_message(message.from_user.id, text=data['text_project_1'])


def back(message) -> None:
    """Функция изменяет кнопки для стартового раздела."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('Простые действия')

    item2 = types.KeyboardButton(data['info_author'])
    item3 = types.KeyboardButton(data['connection_author'])

    markup.add(item2, item3, item1)
    bot.send_message(message.from_user.id, text=data['back'], reply_markup=markup)


def coin(message) -> None:
    """Функция отправляет в чат результат подбрасывания монетки."""
    result = ("Орёл", "Решка")[randint(0, 1)]
    bot.send_message(message.from_user.id, text=result)


def rand_int(message) -> None:
    """Функция запрашивает два числа и передаёт их в функцию get_two_numbers для дальнейших действий."""
    text = f'Введите два числа через пробел. \nПример:\n1 150'
    bot.send_message(message.from_user.id, text=text)
    bot.register_next_step_handler(message, get_two_numbers)


def get_two_numbers(message) -> None:
    """Функция принимает два числа, проверяет их на корректность и отправляет в чат
    случайное число из переданного интервала."""
    lst = tuple(message.text.split())
    if all(map(str.isdigit, lst)) and len(lst) == 2:
        result = randint(*map(int, lst))
        bot.send_message(message.from_user.id, text=f'Всё верно вот ответ!\n{result}')
    else:
        bot.send_message(message.from_user.id,
                         text=f'Некорректный ввод. Для повторного ввода нажмите кнопку {data["rand_int"]}')


def simple_list(message) -> None:
    """Функция запрашивает произвольное число позиционных аргументов и передаёт их
    в функцию get_list для дальнейших действий."""
    text = f'''Данная команда выводит заданное кол-во слов из введённого перечня. Отбор происходит случайным образом.
Введите произвольное кол-во слов через пробел и число.\n\nПример:\nСлово№1 Слово№2 Слово№3 Слово№n 2
\nВывод:\nСлово№3 Слово№4'''
    bot.send_message(message.from_user.id, text=text)
    bot.register_next_step_handler(message, get_list)


def get_list(message) -> None:
    """Функция принимает список, проверяет их на корректность и отправляет в чат
    случайный перечень аргументов, если число аргументов не передано, то будет отправлен в чат один аргумент."""
    try:
        lst = tuple(message.text.split())
        num = 1
        text_error = f'Некорректный ввод. Для повторного ввода нажмите кнопку "{data["simple_list"]}"'
        if lst[-1].isdigit():
            print(lst[-1].isdigit())
            print(lst[-1])
            num, lst = int(lst[-1]), lst[:-1]

        if len(lst) < num:
            text_error = f'''Некорректный ввод, заданное число больше общего списка. 
Для повторного ввода нажмите кнопку "{data["simple_list"]}"'''
            raise Exception

    except Exception:
        bot.send_message(message.from_user.id, text=text_error)
    else:
        result = ', '.join(sample(lst, num))
        bot.send_message(message.from_user.id, text=f'Всё верно вот ответ!\n{result}')


def what_city(message) -> None:
    """Функция запрашивает город и передаёт его в функцию what_is_the_weather для дальнейших действий."""
    text = f'Напишите город \nПример:\nМосква'
    bot.send_message(message.from_user.id, text=text)
    bot.register_next_step_handler(message, what_is_the_weather)


def what_is_the_weather(message) -> None:
    """Функция для запроса погоды на яндекс-погоде через API(не более 50 запросов в день) и отправки в чат."""
    url_weather = 'https://api.weather.yandex.ru/v2/informers'

    headers = {'X-Yandex-API-Key': data["weather_api_key"]}
    geolocator = geocoders.Nominatim(user_agent="app_assis")
    city_fun = message.text.title()

    try:
        latitude = geolocator.geocode(city_fun).latitude
        longitude = geolocator.geocode(city_fun).longitude
        weather_params = {
            'lat': latitude,
            'lon': longitude,
            'lang': 'ru_RU'
        }
    except Exception:
        telegram.notify(token=data["token_bot"], chat_id=data["user_id"],
                        message=f'''Некорректный ввод города. 
                        Для повторного ввода нажмите кнопку {data["weather_report"]}''')

    else:
        response = requests.get(url_weather, headers=headers, params=weather_params)
        data_weather = response.json()

        fact_weather_dict = data_weather['fact']

        result = f"""Прогноз на {dict_part_name_ru['fact']}
    {dict_conditions_ru[fact_weather_dict['condition']].capitalize()}
    Температура: {fact_weather_dict['temp']} ℃
    По ощущениям как {fact_weather_dict['feels_like']} ℃
    Скорость ветра {fact_weather_dict['wind_speed']} м/с

    """

        for part in data_weather['forecast']['parts']:
            result += f"""Прогноз на {dict_part_name_ru[part['part_name']]}
    {dict_conditions_ru[part['condition']].capitalize()}
    Максимальная температура: {part['temp_max']} ℃
    Минимальная температура: {part['temp_min']} ℃
    По ощущениям как {part['feels_like']} ℃
    Скорость ветра {part['wind_speed']} м/с

    """

        link_weather = str(data_weather['info']['url'])

        result += f"Более подробнее тут:\n{link_weather}"
        telegram.notify(token=data["token_bot"], chat_id=data["user_id"], message=result)


db_buttons = {
    data['info_author']: info_author,
    data['info_author_back']: info_author,
    data['knowledge_py']: knowledge_py,
    data['connection_author']: info_me,
    data['course_and_certificate']: course_and_certificate,
    data['projects']: project,
    data['simple_move']: simple_move,
    data['back']: back,
    data['coin']: coin,
    data['rand_int']: rand_int,
    data['weather_report']: what_city,
    data['simple_list']: simple_list
}

bot.polling(none_stop=True)
