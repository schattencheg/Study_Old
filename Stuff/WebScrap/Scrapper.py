import requests
from bs4 import BeautifulSoup

startUrl = "https://www.kinopoisk.ru/lists/top250/?page="
startUrl = "https://hookuphotshot.com/the-girls/page/"
startUrl = "https://hookuphotshot.com/the-girls/page/12/"

proxies = {
'HTTPS':'https://169.57.1.84:8123',
'HTTPS':'https://169.57.1.85:8123',
'HTTPS':'https://169.57.1.84:80',
'HTTPS':'https://169.57.1.85:25',
'HTTPS':'https://84.247.51.123:3128',
'HTTPS':'https://172.96.172.68:3128',
'HTTPS':'https://62.33.207.202:3128',
'HTTPS':'https://62.33.207.202:80',
'HTTPS':'https://159.8.114.37:80',
'HTTPS':'https://159.8.114.37:8123',
'HTTPS':'https://159.8.114.34:8123',
'HTTPS':'https://159.8.114.37:25',
'HTTPS':'https://176.9.85.13:3128',
'HTTPS':'https://95.217.186.24:3128',
'HTTPS':'https://51.91.157.66:80',
'HTTPS':'https://207.38.83.241:3128',
'HTTPS':'https://5.56.132.46:3128',
'HTTPS':'https://136.243.254.196:80',
'HTTPS':'https://84.91.22.240:80',
}

for pageNo in range(1,2):
    url = startUrl + str(pageNo)
    url = startUrl
    page = requests.get(url, proxies)
    soup = BeautifulSoup(page.content, 'html.parser')
    #results = soup.find( id='ResultsContainer')
    job_elems = soup.find_all('div', class_='desktop-rating-selection-film-item')
    for element in job_elems:
        #class="film-item-rating-position__position"
        rating = element.find('div', class_='film-item-rating-position__position')
        #class="selection-film-item-poster__image" src
        url = element.find('div', class_='selection-film-item-poster__image')
        name = element.find('div', class_='selection-film-item-meta__name')
    #print(page)
    print("")
