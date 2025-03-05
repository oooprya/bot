import logging
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types 
from aiogram.dispatcher.filters.state import State, StatesGroup
from time import sleep
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)
bot = Bot(token = "HERE TOKEN")
dp = Dispatcher(bot, storage=MemoryStorage())

class Form(StatesGroup):
    day = State()
    hour = State()
    minutes = State()
    
@dp.message_handler(commands=['alarm'])
async def alarm(message: types.Message):
    await message.answer("Plsm,input day for alarm")
    await Form.day.set()

@dp.message_handler(state=Form.day)
async def answerDay(message: types.Message, state: FSMContext):
    answer_day = message.text

    await state.update_data(answer_day1 = answer_day )

    await message.answer("Plsm,input hour for alarm")
    await Form.hour.set()

@dp.message_handler(state=Form.hour)
async def answerHour(message: types.Message, state: FSMContext):
    answer_hour = message.text

    await state.update_data(answer_hour1 = answer_hour )
    await message.answer("Plsm,input minutes for alarm")
    await Form.minutes.set()

@dp.message_handler(state=Form.minutes)
async def answerMinutes(message: types.Message, state: FSMContext):

    data = await state.get_data()
    answer_day1 =  data.get("answer_day1")
    answer_hour1 = data.get("answer_hour1")
    answer_minutes = message.text    

    while True :
        time_now = datetime.now()
        if str(time_now.hour) == answer_hour1 and str(time_now.minute) == answer_minutes and str(time_now.day) == answer_day1:
            await bot.send_message (message.chat.id, 'time to wake up')
            break
        await asyncio.sleep(1)

    await state.finish()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('This bot help you set the alarm and use API for choice random music.')

@dp.message_handler(commands=['time'])   
async def time_now (message: types.Message):
    time = datetime.now()
    b = time.strftime('Time now is ' + '%H:%M:%S' + '\n' '%A,%d' + '\n'  '%B,  %Y')
    await message.answer(b)

@dp.message_handler(commands=['help'])
async def help (message: types.Message):
    await message.answer(
        text = '''
        This telegram bot was created as an alarm clock that can search for random music and use it to awakening more easily.
        
        /time - show actual time and date now.             
        /alarm - help you set alarm. The format used is 24 hours.
        '''
          )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
