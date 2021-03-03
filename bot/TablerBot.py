from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from aiogram import Bot, Dispatcher, types, executor

from database.serializers import UserSerializer, GroupSerializer, GroupScheduleSerializer
from bot.states import GroupChangeState
from utils.updater import download_schedules, update_schedules

import bot.keyboards as kb
from bot.messages import MESSAGES
from settings import TOKEN

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    if not UserSerializer.is_user(message.from_user.id):
        await message.answer(MESSAGES['unregister_user'])
        await GroupChangeState.first()
    else:
        await message.answer(MESSAGES['start'], reply_markup=kb.main_kb)


@dp.message_handler(commands=['change_group'])
async def change_group(message: types.Message):
    await message.answer('Введите новую группу')
    await GroupChangeState.first()


@dp.message_handler(commands=['cancel'], state="*")
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(MESSAGES['cancel'])


@dp.message_handler(state=GroupChangeState.EnterGroup)
async def enter_group(message: types.Message, state: FSMContext):
    group = GroupSerializer.get_group(message.text)
    if group is None:
        await message.answer(MESSAGES['group_not_found'])
    else:
        UserSerializer.create_or_update_group(user_id=message.from_user.id,
                                              group_id=group.id)
        await message.answer(MESSAGES['group_changed_to'].format(group.name))
        await state.finish()


@dp.message_handler(commands=['menu'])
async def menu(message: types.Message):
    await message.answer(MESSAGES['menu'], reply_markup=kb.main_kb)


@dp.message_handler(text='Внеучебная деятельность')
async def life_schedule(message: types.Message):
    await message.answer_photo(open(r'media/quantized.png', 'rb'))


@dp.message_handler(text='Меню столовой')
async def cafe_menu(message: types.Message):
    await message.answer_document(open(r'media/menu.pdf', 'rb'))


@dp.message_handler(text='Студенческая жизнь')
async def student_life(message: types.Message):
    await message.answer('text', reply_markup=kb.student_life_kb)


@dp.message_handler(text='Студенческий совет')
async def student_council(message: types.Message):
    await message.answer_photo(open(r'media/сouncil.png', 'rb'), caption=MESSAGES['student_council'],
                               reply_markup=kb.st_sov_kb)


@dp.message_handler(text='Расписание')
async def schedule(message: types.Message):
    user_id = message.from_user.id
    if not UserSerializer.is_user(user_id):
        await message.answer("Для получения расписания выберите группу /change_group")
    else:
        group = UserSerializer.get_group(user_id)
        await message.answer(f"Расписание для {group.name}", reply_markup=kb.week_parity_kb())


async def week_day(call: types.CallbackQuery, parity, **kwargs):
    markup = kb.week_day_kb(parity)
    await call.message.edit_reply_markup(markup)


async def show_schedule(call: types.CallbackQuery, parity, day):
    group_id = UserSerializer.get_group(call.from_user.id).id
    _schedule = GroupScheduleSerializer.get_schedule(group_id, parity, day)

    tt = ''
    for pair in _schedule:
        tt += f"{pair}\n"

    if len(_schedule) == 0:
        tt = 'Выходной'

    # await call.message.delete_reply_markup()
    await call.message.answer(tt)


levels = {
    "0": week_day,
    "1": show_schedule
}


@dp.callback_query_handler(kb.week_cd.filter())
async def week_parity_cd(call: types.CallbackQuery, callback_data: dict):
    level = callback_data.get('level')
    parity = callback_data.get('parity')
    day = callback_data.get('day')

    step = levels[level]
    await step(call, parity=parity, day=day)


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if UserSerializer.is_admin(message.from_user.id):
        await message.answer('Админская панель', reply_markup=kb.admin_kb())
    else:
        await message.answer('Недостаточно прав')


@dp.callback_query_handler(kb.admin_cd.filter())
async def admin_panel(call: types.CallbackQuery, callback_data: dict):
    command = callback_data['command']
    # await call.message.delete_reply_markup()

    if command == "0":
        try:
            download_schedules()
            update_schedules()
            await call.answer(MESSAGES['schedule_update'], show_alert=True)
        except:
            await call.answer("Что-то пошло не так...", show_alert=True)
    elif command == "1":
        await call.answer("Админ панель закрыта!")
    else:
        await call.answer("Неизвестная команда")
    await call.message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


def start():
    executor.start_polling(dp, skip_updates=True)
