import os
import requests
from bs4 import BeautifulSoup


def download_category(soup, path, category):

    event_names = []
    event_links = []

    body = soup.find('div', class_='list_wrapper row')

    for event in body.find_all('li'):
        event_year = event.get('data-sid')
        event_name = event_year + ' ' + event.div.a.picture.img.get('alt', '')
        event_names.append(event_name)
        event_links.append(event.div.a.get('href', ''))

    os.chdir(path)
    makeDir('moto')
    makeDir(category)

    for i,event in enumerate(event_links):
        makeDir(event_names[i][:4]) # year-wise folder
        makeDir(event_names[i][5:]) # event per year)
        print(f'{event_names[i][:4]} -> {event_names[i][5:]}')
        content = requests.get(event).text
        image_soup = BeautifulSoup(content, 'lxml')
        download_images(image_soup)
        os.chdir('..')
        os.chdir('..')


def makeDir(folder_name):
    if not os.path.exists(folder_name):
        try:
            os.makedirs(folder_name)
        except Exception as err:
            print(err)
    os.chdir(folder_name)


def download_images(event_soup):
    section = event_soup.find('section', id='links')
    photos = section.find_all('li')
    counter = success = 0
    for pic in photos: 
        title = pic.div.a.get('title', '') 
        # formatting titile to '0NN Image Name' 
        title = str(counter).zfill(2) + ' ' + title + '.jpg'
        dl_link = pic.div.a.get('data-image-fullscreen', '')
        try:
            # saving each image file
            if (not os.path.exists(title)) :
                with open(title, 'wb') as output:
                    output.write(requests.get(dl_link).content)
                    success+=1
        except Exception as err:
            print(err)
        finally:
            counter+=1

    print(f'{success}/{len(photos)} downloaded')


