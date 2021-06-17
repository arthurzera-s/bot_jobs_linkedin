import requests
from bs4 import BeautifulSoup
from time import sleep


def searchJob(link):
    list_jobs = []

    soup = creatingSoup(link)

    jobs = soup.find_all('a')
    for job in jobs:
        dict_job = {}
        classe = job.get('class')
        href = job.get('href')        

        if (classe[0] == 'base-card__full-link'):
            soup_job = creatingSoup(href)
            try:
                dict_job['title'] = soup_job.title.string
            except Exception:
                dict_job['title'] = soup_job.title
            dict_job['link'] = href

            list_jobs.append(dict_job)
    return list_jobs


def creatingSoup(link):
	r = requests.get(link)
	r.encoding = "UTF-8"
	r = r.text
	soup = BeautifulSoup(r, 'html5lib')
	return soup

