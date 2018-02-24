import json
import random
import telepot
# import urllib3
from datetime import datetime, timedelta
import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler

wordstohurry = ['Біжи', 'Ігнеееееет']
mintoles = {8: 27, 10: 22, 12: 17, 14: 12, 16: 7, 18: 0, 20: 0, 22: 0}
active_users = []


def print_lesson(w=0):
    with open("timetable.json", 'r') as f:
        tt = json.load(f)

    logging.info("Timetable loaded")
    curt = datetime.now()+timedelta(hours=2)
    if curt.minute != mintoles[curt.hour]:
        logging.info("Wrong hour-minute pair")
        return

    curday = str(curt.weekday()+1)
    curles = str(curt.hour/2-3)
    logging.info(curday)
    logging.info(curles)
    try:
        for l in tt['data']['weeks'][w]['days'][curday]['lessons']:
            if l['lesson_number'] == curles:
                lesson_name = l['lesson_name']
                room = l['lesson_room']

                text = random.choice(wordstohurry)+' на ' + lesson_name + ' в ' + room
                for u in active_users:
                    bot.sendMessage(u, text)
    except:
        logging.info("No lessons for this time")


def test_scheduler():
    logging.info("I'm working")
    for u in active_users:
        bot.sendMessage(u, str(datetime.now()))


def print_lesson_1_week():
    return print_lesson('1')


def print_lesson_2_week():
    return print_lesson('2')


secret = "909d8761-0bc9-4abd-9c66-a8051862f9c7"
bot = telepot.Bot('496319740:AAEfKfU19jMFgPqo4joU5WLm73dHQGqh8MU')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='super.log',
                    filemode='w')

scheduler = BackgroundScheduler()
# scheduler.add_job(print_lesson_2_week, 'cron', week='*/2', day_of_week='0-5', minute='27,22,17,12,7,48', hour='6,8,10,12,14,16,20')
# scheduler.add_job(print_lesson_1_week, 'cron', week='2-53/2', day_of_week='0-5', minute='27,22,17,12,7,48', hour='6,8,10,12,14,16,20')
scheduler.add_job(test_scheduler, 'cron', minute='*', hour='*')
scheduler.start()


def handle(msg):
    text = msg["text"]
    chat_id = msg["chat"]["id"]

    if text == '/start':
        bot.sendMessage(chat_id, "To registr send me /r")
    elif text == '/r':
        if chat_id not in active_users:
            active_users.append(chat_id)
        bot.sendMessage(chat_id, "Now you will have tons of notifications")

    for u in active_users:
        logging.info(u)


bot.message_loop(handle)
print("Starting...")
while 1:
    time.sleep(2.43)
