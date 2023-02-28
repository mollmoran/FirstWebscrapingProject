import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver

# creating a function to search for html elements and assign the content to variables


def scrape_page(soup, sounds):

    sound_elements = soup.find_all('div', class_='w-full p-3 bg-white dark:bg-gray-900 border '
                                                 'border-secondary-grey-100 shadow-[0_10px_25px_#D9D9D9] '
                                                 'dark:shadow-[0_10px_25px_#565656] dark:border-gray-700 inline-block '
                                                 'rounded-3xl relative flex')

    for sound_element in sound_elements:

        title = sound_element.find('a', class_='font-medium text-black text-md dark:text-white cursor-pointer '
                                                  'block line-clamp-2 leading-5 transition w-[calc('
                                                  '100%_-_24px)]').text

        uploader = sound_element.find('a', class_='text-sm md:text-sm-xs font-medium text-[#C0C0C0] '
                                                  'cursor-pointer whitespace-nowrap overflow-ellipsis overflow-hidden'
                                                  ' block mt-1.5 w-[calc(100%_-_24px)]').text

        views = sound_element.find('span', class_='text-secondary-grey-400 dark:text-white text-sm md:text-xxs ml-1 '
                                                  'mt-0.5 overflow-hidden whitespace-nowrap').text

        likes = sound_element.find('span', class_='text-secondary-grey-400 dark:text-white text-sm md:text-xxs ml-1 '
                                                  'overflow-hidden whitespace-nowrap')

        if likes is not None:
            likes = likes.text
        else:
            likes = 'No likes'

        clip_url = "https://www.voicy.network" + sound_element.find('a', class_='font-medium text-black text-md '
                                                                                'dark:text-white cursor-pointer block'
                                                                                ' line-clamp-2 leading-5 transition '
                                                                                'w-[calc(100%_-_24px)]').get('href')
        page2 = requests.get(clip_url, headers=headers)

        soup2 = BeautifulSoup(page2.text, 'html.parser')

        sound_elements2 = soup2.find_all('p', class_='text-sm dark:text-white')

        for sound_element_detail in sound_elements2:

            creation_date = sound_element_detail.find('p', class_='m-0 text-sm text-secondary-gray-500 dark:text-white').text

            creation_dateedit = creation_date.split('created on')[1].lstrip().split('.')[0]

        sounds.append(
            {
                'title': title,
                'uploader': uploader,
                'views': views,
                'likes': likes,
                'clip_url': clip_url,
                'creation_date': creation_dateedit

            }
        )


# url, can be changed to look for other artists
base_url = 'https://www.voicy.network/search/billie-elish-sound-effects'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (HTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

page = requests.get(base_url, headers=headers)

driver = webdriver.Chrome("C:\\Users\\molly\\PycharmProjects\\webScraper1\\chromedriver.exe")

driver.get(base_url)

# scrolling to the bottom of the page
lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var "
                                  "lenOfPage=document.body.scrollHeight;return lenOfPage;")
match = False

while not match:
    lastCount = lenOfPage
    time.sleep(3)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var "
                                      "lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount == lenOfPage:
        match = True

time.sleep(.5)

soup = BeautifulSoup(driver.page_source, 'html.parser')

sounds = []

scrape_page(soup, sounds)

# creating the csv file and populating it with the sound clip details

csv_file = open('sounds.csv', 'w', encoding='utf-8', newline='')

writer = csv.writer(csv_file)

writer.writerow(['Title', 'Uploader', 'Views', 'Likes', 'Clip URL', 'Creation Date'])

for sound in sounds:
    writer.writerow(sound.values())