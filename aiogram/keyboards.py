from aiogram.utils.callback_data import CallbackData
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, \
    InlineKeyboardButton, InlineKeyboardMarkup

main_kb = ReplyKeyboardMarkup(resize_keyboard=True) \
    .row(KeyboardButton("Расписание"), KeyboardButton("Внеучебная деятельность")) \
    .row(KeyboardButton("Студенческая жизнь"), KeyboardButton("GASU MEDIA HOUSE")) \
    .row(KeyboardButton("Меню столовой"), KeyboardButton("Графики выдачи"))

student_life_kb = ReplyKeyboardMarkup(resize_keyboard=True) \
    .row(KeyboardButton("Студенческий совет"), KeyboardButton("Проекты")) \
    .row(KeyboardButton("Кирпич"), KeyboardButton("Волонтёрство")) \
    .row(KeyboardButton("Стройотряды"), KeyboardButton("Назад"))

# Меню выбота чётности недели
week_cd = CallbackData("week", "level", "parity", "day")
admin_cd = CallbackData("admin", "command")


def get_week_cd(level="0", parity="0", day="0"):
    return week_cd.new(level=level, parity=parity, day=day)


def get_admin_cd(command):
    return admin_cd.new(command=command)


def week_parity_kb():
    return InlineKeyboardMarkup(resize_keyboard=True) \
        .add(InlineKeyboardButton("Числитель", callback_data=get_week_cd(level="0", parity="1")),
             InlineKeyboardButton("Знаменатель", callback_data=get_week_cd(level="0", parity="2")))


# Меню выбора дня недили
def week_day_kb(parity):
    return InlineKeyboardMarkup(resize_keyboard=True) \
        .row(InlineKeyboardButton("Понедельник", callback_data=get_week_cd(level="1", parity=parity, day="1")),
             InlineKeyboardButton("Вторник", callback_data=get_week_cd(level="1", parity=parity, day="2"))) \
        .row(InlineKeyboardButton("Среда", callback_data=get_week_cd(level="1", parity=parity, day="3")),
             InlineKeyboardButton("Четверг", callback_data=get_week_cd(level="1", parity=parity, day="4"))) \
        .row(InlineKeyboardButton("Пятница", callback_data=get_week_cd(level="1", parity=parity, day="5")),
             InlineKeyboardButton("Суббота", callback_data=get_week_cd(level="1", parity=parity, day="6")))


def admin_kb():
    return InlineKeyboardMarkup() \
        .row(InlineKeyboardButton("Обновить расписание", callback_data=get_admin_cd("0"))) \
        .row(InlineKeyboardButton("Отмена", callback_data=get_admin_cd("1")))


st_sov_kb = InlineKeyboardMarkup().add(InlineKeyboardButton('Перейти', url='https://vk.com/ssspbgasu'))
