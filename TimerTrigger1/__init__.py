import datetime
import logging

from bs4 import BeautifulSoup
import requests
import telegram

import azure.functions as func

TOKEN = ""
CHAT_ID = 0

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    send_message()

def find_vax():
    cities = open("cities.txt","r")
    city_list = cities.readlines()
    
    response = requests.get("https://www.vaccinespotter.org/CA/index.html")

    soup = BeautifulSoup(response.text, "html.parser")
    pharmacies = soup.find_all("div", {"class": "location-result"})

    text = set()

    for pharmacy in pharmacies:
        location = pharmacy.find("h5", {"class": "mb-0"}).getText()
        #url = pharmacy.find("a", {"class": "btn"})['href']
        for city in city_list:
            if city.strip() == "":
                continue
            #print(city.strip(), location)
            if city.strip().upper() in location.upper() and "VISALIA" not in location.upper():
                text.add("{}".format(location))
                #print("{} - {}".format(location,url))
    return text

def send_message():
    bot = telegram.Bot(token = TOKEN)
    r = find_vax()
    txt = ""
    for v in r:
        txt += v.replace('\n', ' ').replace('    ', ' ').replace('   ', ' ').strip() + "\n"
    print(txt)
    if txt.strip() != "":
        bot.sendMessage(chat_id = CHAT_ID, text = txt.strip())
    else:
        bot.sendMessage(chat_id = CHAT_ID, text="No vaccines found :(")
    
#send_message()
