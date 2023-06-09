# import csv
# from pygame import mixer
# import pyttsx3
import json

# Переменные
name_file = 'file.json'

with open(name_file, 'r', encoding='utf-8') as file_json:
    data = json.load(file_json)

dict_command = {
    data['what_author_knows']: data['text_knowledge'],
    data['curriculum']: data['text_training_plan'],
    data['personal_skills']: data['text_personal_skills'],
    data['goals_tasks']: data['target_goal'],
    data['last_work']: data['text_last_work'],
}

# Название файлов и пути
path_certificate = 'certificate/'
name_txt_file = 'phonebook_company.txt'
name_csv_file = 'phonebook_company.csv'


def write_info(text: str) -> None:
    """Функция для записи данных о том кто общался с ботом при условии, что человек согласился Познакомиться.
    Если он уже есть в базе, то добавление не происходит."""
    with open(name_txt_file, 'r+', encoding='utf-8') as file_w:
        generator_data = (i.strip() for i in file_w.readlines())
        if not (text.strip() in generator_data):
            file_w.write(text)  # для  txt файла
            # csv.writer(file).writerow(text)


def get_info(message) -> str:
    """Функция возвращает строку определённого формата с содержанием информации о написавшем."""
    return f"""\nВот информация: 
    ID: {message.from_user.id};
    FIRST_NAME: {message.from_user.first_name};
    LAST_NAME: {message.from_user.last_name};
    USERNAME: {message.from_user.username}."""


def get_text_for_write(message) -> str:
    """Функция возвращает строку с информацией о написавшем для дальнейшей записи в файл."""
    user = message.from_user
    return f'{", ".join(map(str, (user.id, user.first_name, user.last_name, user.username)))}'


# def look_in_notebook(file_name):
#     """Функция для открытия файла с именами и компаниями, ранее написавших представителей компаний
#     для дальнейшей проверки, что бот с ним уже общался."""
#     with open(file_name, 'r', encoding='utf-8') as file:
#         columns_name = file.readline().strip().split(',')
#         text_all = [line.strip().split(',') for line in file.readlines()]  # file.read().strip().split('\n')
#         dt = {}
#         for i in columns_name:
#             for j in range(len(text_all)):
#                 dt[i] = dt.get(i, []) + [text_all[j][columns_name.index(i)].lower()]
#     return dt

# # Для csv файла
# with open(file_name, 'r') as file:
#     text = list(csv.reader(file, delimiter=','))
#     name = [i.lower() for i in text[0]]
#     dt = {}
#     for i in name:
#         for j in range(1, len(text)):
#             dt[i] = dt.get(i, []) + [text[j][name.index(i)].lower()]
# return dt
#
# def read_text(say):
#     """Функция для озвучки текста, работает только если общаться с ботом на ПК."""
#     tts = pyttsx3.init()
#
#     tts.say(say)
#     tts.runAndWait()
#
# tts.endLoop()  # add this line
# tts.stop()
#
# voices = engine.getProperty('voices')
# # engine.setProperty('volume',1.0)
# engine.setProperty('voice', voices[1].id)
# engine.setProperty('rate', 200)  # setting up new voice rate
# outfile = "temp.wav"
# engine.save_to_file(say, outfile)
# engine.runAndWait()
#
# mixer.init()
# mixer.music.load("temp.wav")
# mixer.music.stop()
# mixer.music.play()
