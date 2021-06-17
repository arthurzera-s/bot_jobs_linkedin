import requests
import json
import os
from time import sleep
from scraping import searchJob


TOKEN_BOT = "1784193017:AAEy81S6CQWBtTghhxaU3i4rbrVVTUdQ0Zc"
URL_BASE = f'https://api.telegram.org/bot{TOKEN_BOT}'
FILE_NAME = 'registered.txt'


def main():
	updates = getUpdate()
	if len(updates) >= 1:
		handlingUpdates(updates)
	

def handlingUpdates(updates):
	for update in updates:
		_id = update['message']['chat']['id']
		text = update['message']['text']
		user_name = update['message']['chat']['first_name']
		offset = update['update_id']
		
		if text.lower() == '/start':
			if checkID(f'{_id}\n', FILE_NAME) == False:
				print("Novo usuário cadastrado!")
				sendWelcome(_id, user_name)
				addID(_id, FILE_NAME)
		
		elif checkID(f'{_id}\n', FILE_NAME):
			getJobs(text, _id)
			print("Nova pesquisa de vagas.")
			
		url = f'{URL_BASE}/getUpdates?offset={offset+1}'
		r = requests.get(url)
		


def getJobs(_key, _id):
	message = f"Estou procurando as principais vagas relacionadas a {_key.upper()} no LinkedIn.\n Aguarde alguns instantes!"
	url = f'{URL_BASE}/sendMessage?chat_id={_id}&text={message}'
	requests.get(url)

	link = f"https://www.linkedin.com/jobs/search/?geoId=106057199&keywords={_key}&location=Brasil"
	list_jobs = searchJob(link)
	for job in list_jobs:
		title = job['title']
		link_job = job['link']

		message = f"{title}\n\nVeja mais em:\n{link_job}"
		url = f'{URL_BASE}/sendMessage?chat_id={_id}&text={message}'
		requests.get(url)
		sleep(5)

	message = f"Para buscar novas vagas em outras tecnologias digitar a tecnologia desejada!"
	url = f'{URL_BASE}/sendMessage?chat_id={_id}&text={message}'
	requests.get(url)


def getUpdate():
	url = f'{URL_BASE}/getUpdates'
	r = requests.get(url)
	update = json.loads(r.text)
	update =  update['result']
	return update


def sendWelcome(_id, name):
	message = f"Olá, {name}! Sou um bot que busca vagas no LinkedIn!\nPor favor, digite qual a área de seu interesse:\n\n👨‍💻 Qualquer dúvida entre em contato com: @arthurzera"
	url = f'{URL_BASE}/sendMessage?chat_id={_id}&text={message}'
	requests.get(url)


def sendInvalidCommand(_id):
	message = f"Comando inválido. Para receber as vagas digite /start.\n\n👨‍💻 Qualquer dúvida entre em contato com: @arthurzera"
	url = f'{URL_BASE}/sendMessage?chat_id={_id}&text={message}'
	requests.get(url)


def checkID(_id, name):
	file = open(name, 'r')
	list_id = file.readlines()

	if _id in list_id:
		return True
	else:
		return False
	file.close()


def addID(_id, name):
	file = open(name, 'a')
	file.write(f'{_id}\n')
	file.close()


while True:
	main()
	sleep(3)