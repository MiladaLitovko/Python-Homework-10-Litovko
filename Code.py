from cmath import log
from email.message import Message
import telebot
import os
import datetime


first=""
second=""
script_dir = os.path.dirname(__file__)

history  = []

logProgr = ""
history_for_bot = open(script_dir + '/history_for_bot.txt','r', encoding='utf-8')
for mess in history_for_bot:
    history.append(mess)
history_for_bot.close()

bot = telebot.TeleBot('5460917203:AAFcw5YBaPs57Q9f6elHGP1HRVkjbaus1No')

del_buttons = telebot.types.ReplyKeyboardRemove()
 
buttons1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons1.row(telebot.types.KeyboardButton('Комплексные'),
             telebot.types.KeyboardButton('Рациональные'),)
buttons1.row(telebot.types.KeyboardButton('Ещё не определился'))
 
buttons2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons2.row(telebot.types.KeyboardButton('+'),
             telebot.types.KeyboardButton('-'))
buttons2.row(telebot.types.KeyboardButton('*'),
             telebot.types.KeyboardButton('/'))


def message(chat_id, text, reply_markup = None):
    bot.send_message(chat_id=chat_id,
                text=text,
                reply_markup=reply_markup)
    time_of_message = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
    history.append(time_of_message + " БОТ:" + str(text) + '\n')


@bot.message_handler(commands=['log'])
def hello(msg: telebot.types.Message):
    logP = ''
    for line in history:
        logP += line
    message(chat_id=msg.from_user.id,
                     text='Лог программы: \n' + logP,
                     reply_markup=del_buttons)
    
 
@bot.message_handler()
def hello(msg: telebot.types.Message):
    message(chat_id=msg.from_user.id,
                     text='Здравствуйте.\nВыберите режим работы калькулятора.',
                     reply_markup=buttons1)
    bot.register_next_step_handler(msg, answer)
 
 
def answer(msg: telebot.types.Message):
    time_of_message = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
    history.append(time_of_message + " USER:" + msg.text + '\n')
    if msg.text == 'Комплексные':
        bot.register_next_step_handler(msg, second_msg)
        message(chat_id=msg.from_user.id,
                         text='Введите первое число',
                         reply_markup=del_buttons)
    elif msg.text == 'Рациональные':
        bot.register_next_step_handler(msg, second_msg)
        message(chat_id=msg.from_user.id,
                         text='Введите первое число.',
                         reply_markup=del_buttons)
    elif msg.text == 'Ещё не определился':
        bot.register_next_step_handler(msg, answer)
        message(chat_id=msg.from_user.id, text='Возвращайтесь, когда определитесь.')
    else:
        bot.register_next_step_handler(msg, answer)
        message(chat_id=msg.from_user.id, text='Пожалуйста, используйте кнопки.')
        message(chat_id=msg.from_user.id, text='Выберите режим работы калькулятора.', reply_markup=buttons1)
 

def second_msg(msg: telebot.types.Message):
    time_of_message = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
    history.append(time_of_message + " USER:" + msg.text + '\n')
    global first
    if 'j' in msg.text or 'i' in msg.text:
        first=complex("".join(msg.text.split()).replace('i','j'))
    else:
        first = float(msg.text.replace(',','.'))
    bot.register_next_step_handler(msg,sign)
    message(chat_id=msg.from_user.id,
                         text='Введите второе число.',
                         reply_markup=del_buttons)


def sign(msg: telebot.types.Message):
    time_of_message = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
    history.append(time_of_message + " USER:" + msg.text + '\n')
    global second
    if 'j' in msg.text or 'i' in msg.text:
        second=complex("".join(msg.text.split()).replace('i','j'))
    else:
        second = float(msg.text.replace(',','.'))
    bot.register_next_step_handler(msg,counter)
    message(chat_id=msg.from_user.id,text='Введите знак', reply_markup=buttons2)


def counter(msg: telebot.types.Message):
    time_of_message = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
    history.append(time_of_message + " USER:" + msg.text + '\n')
    message(chat_id=msg.from_user.id, text='Ответ: ', reply_markup=del_buttons)
    if msg.text == "+":
        message(chat_id=msg.from_user.id, text=second + first)
    if msg.text == "-":
        message(chat_id=msg.from_user.id, text=first - second)
    if msg.text == "*":
        message(chat_id=msg.from_user.id, text=first * second)
    if msg.text == "/":
        message(chat_id=msg.from_user.id, text=first / second)


bot.polling()

history_for_bot = open(script_dir + '/history_for_bot.txt','w', encoding='utf-8')
for line in history:
    history_for_bot.write(line)
history_for_bot.close()
