import datetime
import logging

from bs4 import BeautifulSoup
import requests
import telegram

import azure.functions as func

TOKEN = "1607636123:AAHDoL4vzfMEqN_7cTzV23EfbP4w5WyNSTA"
CHAT_ID = 696616511

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
    pharmacies = soup.find_all("div", {"class": "mb-4"})

    text = set()

    for pharmacy in pharmacies:
        location = pharmacy.find("h5", {"class": "card-header"}).getText()
        url = pharmacy.find("a", {"class": "btn"})['href']
        for city in city_list:
            if city.strip() == "":
                continue
            #print(city.strip(), location)
            if city.strip().upper() in location.upper():
                text.add("{} - {}".format(location,url))
                #print("{} - {}".format(location,url))
    return text

def send_message():
    bot = telegram.Bot(token = TOKEN)
    r = find_vax()
    txt = ""
    for v in r:
        txt += v + "\n"
    bot.sendMessage(chat_id = CHAT_ID, text = txt.strip())