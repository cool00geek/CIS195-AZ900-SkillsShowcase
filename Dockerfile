FROM python:3.8

WORKDIR /opt
COPY . .
RUN pip3 install requests beautifulsoup4 python-telegram-bot

CMD ["python3", "vax.py"]
