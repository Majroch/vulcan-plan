#!/usr/bin/env python3
from vulcan import Vulcan
import json, datetime, time
from CalDavManager import CalDavManager
from Config import Config

config = Config("main.cfg")
caldav = CalDavManager(config)

try:
    with open(config.get("cert"), "r") as file:
        cert = json.load(file)
except FileNotFoundError:
    print("Cannot find Cert! Creating one:")
    token = input("Enter Token: ")
    symbol = input("Enter Symbol: ")
    pin = input("Enter PIN: ")

    cert = Vulcan.register(token, symbol, pin)

    if cert != None:
        with open(config.get("cert"), "w") as file:
            file.write(json.dumps(cert.json))
    else:
        print("No cert found!")
        exit()
    
vulcan = Vulcan(cert)

while True:
    dates = []
    for x in range(30):
        dates.append(datetime.date.today() + datetime.timedelta(days=x))

    lessons = []
    for date in dates:
        for lesson in vulcan.get_lessons(date=date):
            if lesson.group == "Grupa " + config.get("group") or lesson.group == None:
                lessons.append(lesson)

    events = []
    for lesson in lessons:
        if lesson:
            events.append(caldav.createLessonEvent(lesson))

    for event in events:
        if event:
            if caldav.sendEvent(event):
                print("Sent!")
                time.sleep(1)

    caldav.compareEvents(events)

    print("Sleep for 1 hour!")
    time.sleep(3600)
